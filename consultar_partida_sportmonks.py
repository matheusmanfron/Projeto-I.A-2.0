"""Consulta uma partida específica na Sportmonks pelo fixture_id.

Uso recomendado (PowerShell):
    $env:SPORTMONKS_API_TOKEN = "SEU_TOKEN"
    python consultar_partida_sportmonks.py 19722806
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


URL_BASE = "https://api.sportmonks.com/v3/football/fixtures"


def consultar_partida(fixture_id: int, token: str) -> dict:
    """Consulta a API e devolve somente o objeto da partida."""
    url = f"{URL_BASE}/{fixture_id}"
    parametros = {
        "api_token": token,
        "include": "participants;statistics;scores",
    }

    url_completa = f"{url}?{urlencode(parametros)}"

    try:
        with urlopen(url_completa, timeout=30) as resposta:
            corpo = json.loads(resposta.read().decode("utf-8"))
    except HTTPError as erro:
        detalhe = erro.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Erro HTTP {erro.code}: {detalhe}") from erro
    except URLError as erro:
        raise RuntimeError(f"Não foi possível acessar a API: {erro.reason}") from erro
    except TimeoutError as erro:
        raise RuntimeError("A consulta demorou demais e foi interrompida.") from erro
    except json.JSONDecodeError as erro:
        raise RuntimeError("A API retornou uma resposta que não é um JSON válido.") from erro

    if "data" not in corpo:
        raise RuntimeError("A resposta da API não contém o campo 'data'.")

    return corpo["data"]


def exibir_resumo(partida: dict) -> None:
    """Mostra os campos mais importantes da partida no terminal."""
    participantes = partida.get("participants") or []
    nomes = [p.get("name", "Nome desconhecido") for p in participantes]
    estatisticas = partida.get("statistics") or []
    placares = partida.get("scores") or []

    print("\n--- RESUMO DA PARTIDA ---")
    print(f"Fixture ID: {partida.get('id')}")
    print(f"Data: {partida.get('starting_at')}")
    print(f"State ID: {partida.get('state_id')}")
    print(f"Resultado: {partida.get('result_info')}")
    print(f"Participantes: {' x '.join(nomes) if nomes else 'não informados'}")
    print(f"Registros de placar: {len(placares)}")
    print(f"Registros de estatísticas: {len(estatisticas)}")

    if not estatisticas:
        print("Atenção: a API não retornou estatísticas para esta partida.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Consulta uma partida da Sportmonks pelo fixture_id."
    )
    parser.add_argument("fixture_id", type=int, help="ID da partida na Sportmonks")
    parser.add_argument(
        "--token",
        help="Token da Sportmonks. Prefira usar SPORTMONKS_API_TOKEN.",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        help="Caminho opcional do JSON. Padrão: partida_<fixture_id>.json",
    )
    args = parser.parse_args()

    token = args.token or os.getenv("SPORTMONKS_API_TOKEN")
    if not token:
        parser.error(
            "Token não informado. Defina SPORTMONKS_API_TOKEN ou use --token."
        )

    try:
        partida = consultar_partida(args.fixture_id, token)
    except RuntimeError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        sys.exit(1)

    exibir_resumo(partida)

    arquivo_saida = args.saida or Path(f"partida_{args.fixture_id}.json")
    arquivo_saida.write_text(
        json.dumps(partida, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Resposta completa salva em: {arquivo_saida.resolve()}")


if __name__ == "__main__":
    main()
