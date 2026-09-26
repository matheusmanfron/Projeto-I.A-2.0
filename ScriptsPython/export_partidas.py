"""Consulta partidas de um time na Sportmonks e exporta no formato do projeto.

Exemplo no PowerShell:
    # Preencha SPORTMONKS_API_TOKEN no arquivo .env uma única vez.
    python exportar_partidas_sportmonks_csv.py 53 --inicio 2023-07-01 --fim 2026-06-30
"""

import argparse
import csv
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

URL_BASE = "https://api.sportmonks.com/v3/football/fixtures/between"

# type_id da Sportmonks -> nome utilizado nos CSVs do projeto
TIPOS_ESTATISTICAS = {
    34: "Escanteios",
    45: "Posse de bola (%)",
    52: "Gols",
    79: "Assistências",
    83: "Cartões vermelhos",
    84: "Cartões amarelos",
    1605: "Dribles bem-sucedidos (%)",
}

COLUNAS = [
    "fixture_id",
    "data",
    "partida",
    "time",
    "team_id",
    "local_visitante",
    "adversario",
    "adversario_id",
    "resultado",
    "league_id",
    "season_id",
    "state_id",
    "Escanteios",
    "Posse de bola (%)",
    "Gols",
    "Assistências",
    "Cartões vermelhos",
    "Cartões amarelos",
    "Dribles bem-sucedidos (%)",
]


def carregar_env(caminho: Path) -> None:
    """Carrega pares CHAVE=VALOR de um .env sem dependências externas."""
    if not caminho.exists():
        return

    for numero_linha, linha_original in enumerate(
        caminho.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        linha = linha_original.strip()
        if not linha or linha.startswith("#"):
            continue
        if "=" not in linha:
            raise RuntimeError(
                f"Linha {numero_linha} inválida no arquivo {caminho.name}."
            )

        chave, valor = linha.split("=", 1)
        chave = chave.strip()
        valor = valor.strip()

        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in {'"', "'"}:
            valor = valor[1:-1]

        # Uma variável já definida no sistema tem prioridade sobre o .env.
        os.environ.setdefault(chave, valor)


def consultar_api(
    token: str,
    team_id: int,
    inicio: str,
    fim: str,
    por_pagina: int,
    league_id: int,
) -> tuple[list[dict], int]:
    """Consulta a API em janelas de até 100 dias e devolve (partidas, total_consultas)."""
    try:
        data_inicial = date.fromisoformat(inicio)
        data_final = date.fromisoformat(fim)
    except ValueError as erro:
        raise RuntimeError("As datas devem estar no formato YYYY-MM-DD.") from erro

    if data_inicial > data_final:
        raise RuntimeError("A data inicial não pode ser posterior à data final.")

    todas_partidas = []
    total_consultas = 0
    inicio_intervalo = data_inicial

    while inicio_intervalo <= data_final:
        # A API aceita no máximo 100 dias por consulta (início e fim inclusos).
        fim_intervalo = min(
            inicio_intervalo + timedelta(days=99),
            data_final,
        )

        pagina = 1

        while True:
            parametros = {
                "api_token": token,
                "order": "asc",
                "per_page": min(por_pagina, 50),
                "page": pagina,
                "filters": f"fixtureLeagues:{league_id}",
                "include": "participants;statistics;scores",
            }

            url = (
                f"{URL_BASE}/"
                f"{inicio_intervalo.isoformat()}/"
                f"{fim_intervalo.isoformat()}/"
                f"{team_id}?"
                f"{urlencode(parametros)}"
            )

            total_consultas += 1

            print(
                f"Consulta {total_consultas:02d}: "
                f"{inicio_intervalo} até {fim_intervalo}, "
                f"página {pagina}"
            )

            try:
                with urlopen(url, timeout=60) as resposta:
                    corpo = json.loads(resposta.read().decode("utf-8"))
            except HTTPError as erro:
                detalhe = erro.read().decode("utf-8", errors="replace")[:500]
                raise RuntimeError(f"Erro HTTP {erro.code}: {detalhe}") from erro
            except URLError as erro:
                raise RuntimeError(
                    f"Não foi possível acessar a API: {erro.reason}"
                ) from erro
            except TimeoutError as erro:
                raise RuntimeError(
                    "A consulta demorou demais e foi interrompida."
                ) from erro
            except json.JSONDecodeError as erro:
                raise RuntimeError("A API não retornou um JSON válido") from erro

            dados = corpo.get("data")

            # Janela sem jogos: a API pode omitir o campo 'data'.
            if dados is None:
                dados = []

            if not isinstance(dados, list):
                raise RuntimeError("A resposta não contém uma lista no campo 'data'.")

            todas_partidas.extend(dados)

            rate_limit = corpo.get("rate_limit") or {}

            if rate_limit:
                print(
                    "Consultas restantes:",
                    rate_limit.get("remaining", "não informado"),
                )

            paginacao = corpo.get("pagination") or {}

            if not paginacao.get("has_more", False):
                break

            pagina += 1
            sleep(0.2)

        # Avança para a próxima janela de datas.
        inicio_intervalo = fim_intervalo + timedelta(days=1)

    # Deduplica e ordena somente depois de percorrer todas as janelas.
    partidas_unicas = {
        partida["id"]: partida
        for partida in todas_partidas
        if partida.get("id") is not None
    }

    partidas_ordenadas = sorted(
        partidas_unicas.values(),
        key=lambda partida: partida.get("starting_at", ""),
    )

    return partidas_ordenadas, total_consultas


def localizar_participantes(partida: dict, team_id: int) -> tuple[dict, dict]:
    participantes = partida.get("participants") or []
    time = next((p for p in participantes if p.get("id") == team_id), None)
    adversario = next((p for p in participantes if p.get("id") != team_id), None)
    if not time or not adversario:
        raise ValueError("participantes da partida não foram identificados")
    return time, adversario


def obter_local(participante: dict) -> str:
    """Converte home/away para o padrão já utilizado no projeto."""
    local = (participante.get("meta") or {}).get("location", "")
    return local if local in {"home", "away"} else ""


def extrair_estatisticas(partida: dict, team_id: int) -> dict:
    valores = {nome: "" for nome in TIPOS_ESTATISTICAS.values()}

    for estatistica in partida.get("statistics") or []:
        if estatistica.get("participant_id") != team_id:
            continue

        nome_coluna = TIPOS_ESTATISTICAS.get(estatistica.get("type_id"))
        if not nome_coluna:
            continue

        data = estatistica.get("data") or {}
        valores[nome_coluna] = data.get("value", "")

    return valores


def obter_placar_atual(partida: dict) -> dict[int, int]:
    """Retorna {participant_id: gols} usando somente o placar total CURRENT."""
    placar = {}
    for registro in partida.get("scores") or []:
        if str(registro.get("description", "")).upper() != "CURRENT":
            continue

        participant_id = registro.get("participant_id")
        gols = (registro.get("score") or {}).get("goals")
        if participant_id is not None and isinstance(gols, (int, float)):
            placar[participant_id] = int(gols)
    return placar


def classificar_resultado(
    partida: dict, team_id: int, nome_time: str, adversario_id: int
) -> int | str:
    """Classifica o resultado pela perspectiva do time: 0, 1 ou 2."""
    placar = obter_placar_atual(partida)
    gols_time = placar.get(team_id)
    gols_adversario = placar.get(adversario_id)

    if gols_time is not None and gols_adversario is not None:
        if gols_time > gols_adversario:
            return 2
        if gols_time == gols_adversario:
            return 1
        return 0

    # Fallback para respostas antigas ou partidas sem score CURRENT.
    texto = str(partida.get("result_info") or "").strip().casefold()
    nome_normalizado = nome_time.strip().casefold()

    if "draw" in texto:
        return 1
    if texto.startswith(nome_normalizado) and "won" in texto:
        return 2
    if "won" in texto:
        return 0
    return ""


def formatar_partida(partida: dict, team_id: int) -> dict:
    time, adversario = localizar_participantes(partida, team_id)
    local_time = obter_local(time)

    if local_time == "home":
        nome_partida = f"{time.get('name')} vs {adversario.get('name')}"
    elif local_time == "away":
        nome_partida = f"{adversario.get('name')} vs {time.get('name')}"
    else:
        nome_partida = partida.get("name") or ""

    linha = {
        "fixture_id": partida.get("id", ""),
        "data": partida.get("starting_at", ""),
        "partida": nome_partida,
        "time": time.get("name", ""),
        "team_id": team_id,
        "local_visitante": local_time,
        "adversario": adversario.get("name", ""),
        "adversario_id": adversario.get("id", ""),
        "resultado": classificar_resultado(
            partida,
            team_id,
            time.get("name", ""),
            adversario.get("id"),
        ),
        "league_id": partida.get("league_id", ""),
        "season_id": partida.get("season_id", ""),
        "state_id": partida.get("state_id", ""),
    }
    linha.update(extrair_estatisticas(partida, team_id))
    return linha


def tem_estatisticas_do_time(partida: dict, team_id: int) -> bool:
    return any(
        estatistica.get("participant_id") == team_id
        for estatistica in partida.get("statistics") or []
    )


def main() -> None:
    pasta_script = Path(__file__).resolve().parent
    try:
        carregar_env(pasta_script / ".env")
    except RuntimeError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Exporta partidas da Sportmonks no formato CSV do projeto."
    )
    parser.add_argument("team_id", type=int, help="ID do time, como 53 ou 62")

    parser.add_argument(
        "--inicio",
        default="2023-07-01",
        help="Data inicial no formato YYYY-MM-DD",
    )

    parser.add_argument(
        "--fim",
        default="2026-06-30",
        help="Data final no formato YYYY-MM-DD",
    )

    parser.add_argument(
        "--liga-id",
        type=int,
        default=501,
        help="ID da competição, 501 é a Scottish Premiership",
    )

    parser.add_argument(
        "--por-pagina",
        type=int,
        default=50,
        help="Quantidade consultada na API por página (50)",
    )
    parser.add_argument(
        "--incluir-sem-estatisticas",
        action="store_true",
        help="Também inclui partidas que não possuem estatísticas",
    )
    parser.add_argument(
        "--incluir-nao-finalizadas",
        action="store_true",
        help="Também inclui partidas cujo state_id não é 5",
    )
    parser.add_argument("--token", help="Token; prefira SPORTMONKS_API_TOKEN")
    parser.add_argument("--saida", type=Path, help="Nome do CSV de saída")
    args = parser.parse_args()

    token = args.token or os.getenv("SPORTMONKS_API_TOKEN")
    if not token:
        parser.error(
            "Token não encontrado. Preencha SPORTMONKS_API_TOKEN no arquivo .env."
        )
    if token in {"COLE_SEU_NOVO_TOKEN_AQUI", "SEU_TOKEN", "SECRETO"}:
        parser.error("Substitua o valor de exemplo no .env pelo seu novo token.")
    if not 1 <= args.por_pagina <= 50:
        parser.error("--por-pagina deve estar entre 1 e 50.")

    try:
        partidas, total_consultas = consultar_api(
            token=token,
            team_id=args.team_id,
            inicio=args.inicio,
            fim=args.fim,
            por_pagina=args.por_pagina,
            league_id=args.liga_id,
        )

        selecionadas = []
        ignoradas = []
        for partida in partidas:
            motivo = None
            if not args.incluir_nao_finalizadas and partida.get("state_id") != 5:
                motivo = f"state_id={partida.get('state_id')}"
            elif not args.incluir_sem_estatisticas and not tem_estatisticas_do_time(
                partida, args.team_id
            ):
                motivo = "sem estatísticas"

            if motivo:
                ignoradas.append((partida.get("id"), motivo))
                continue

            linha = formatar_partida(partida, args.team_id)
            if linha["resultado"] == "":
                ignoradas.append(
                    (partida.get("id"), "resultado não identificado com segurança")
                )
                continue

            selecionadas.append(linha)
    except (RuntimeError, ValueError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        sys.exit(1)

    saida = args.saida or Path(f"time_{args.team_id}_partidas_estatisticas.csv")
    with saida.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(selecionadas)

    print(f"\nConsultas realizadas: {total_consultas}")
    print(f"Partidas únicas recebidas: {len(partidas)}")
    print(f"Partidas válidas gravadas: {len(selecionadas)}")
    print(f"Arquivo criado: {saida.resolve()}")

    if ignoradas:
        print("\nPartidas ignoradas:")
        for fixture_id, motivo in ignoradas:
            print(f"- {fixture_id}: {motivo}")


if __name__ == "__main__":
    main()
