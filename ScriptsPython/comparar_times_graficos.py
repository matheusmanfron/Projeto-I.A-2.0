"""Compara dois times a partir dos CSVs gerados no projeto Fut Analytics.

Exemplo:
    python comparar_times_graficos.py celtic_partidas_novas.csv rangers_partidas_novas.csv
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


COLUNAS_OBRIGATORIAS = [
    "time",
    "resultado",
    "Escanteios",
    "Posse de bola (%)",
    "Gols",
    "Assistências",
    "Cartões vermelhos",
    "Cartões amarelos",
    "Dribles bem-sucedidos (%)",
]

ESTATISTICAS_CONTAGEM = [
    "Escanteios",
    "Gols",
    "Assistências",
    "Cartões amarelos",
    "Cartões vermelhos",
]

ESTATISTICAS_PERCENTUAIS = [
    "Posse de bola (%)",
    "Dribles bem-sucedidos (%)",
]

CORES = ["#1B5E9A", "#D97706"]


def carregar_csv(caminho: Path) -> pd.DataFrame:
    """Lê e valida um CSV do projeto."""
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    df = pd.read_csv(caminho, encoding="utf-8-sig")
    ausentes = [coluna for coluna in COLUNAS_OBRIGATORIAS if coluna not in df.columns]
    if ausentes:
        raise ValueError(
            f"O arquivo {caminho.name} não possui as colunas: {', '.join(ausentes)}"
        )
    if df.empty:
        raise ValueError(f"O arquivo {caminho.name} não possui partidas.")

    for coluna in ESTATISTICAS_CONTAGEM + ESTATISTICAS_PERCENTUAIS:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df


def nome_do_time(df: pd.DataFrame, caminho: Path) -> str:
    nomes = df["time"].dropna().astype(str).str.strip()
    if nomes.empty:
        return caminho.stem
    return nomes.mode().iloc[0]


def resultado_padronizado(valor, nome_time: str):
    """Aceita o resultado numérico novo e também os textos dos CSVs antigos."""
    if pd.isna(valor):
        return np.nan

    texto = str(valor).strip()
    try:
        numero = int(float(texto))
        return numero if numero in {0, 1, 2} else np.nan
    except ValueError:
        texto_normalizado = texto.casefold()
        if "draw" in texto_normalizado:
            return 1
        if texto_normalizado.startswith(nome_time.casefold()) and "won" in texto_normalizado:
            return 2
        if "won" in texto_normalizado:
            return 0
        return np.nan


def resumir(df: pd.DataFrame, nome_time: str) -> dict:
    resultados = df["resultado"].apply(
        lambda valor: resultado_padronizado(valor, nome_time)
    )
    return {
        "resultados": {
            "Vitórias": int((resultados == 2).sum()),
            "Empates": int((resultados == 1).sum()),
            "Derrotas": int((resultados == 0).sum()),
        },
        "medias_contagem": df[ESTATISTICAS_CONTAGEM].mean().to_dict(),
        "medias_percentuais": df[ESTATISTICAS_PERCENTUAIS].mean().to_dict(),
        "cobertura": df[ESTATISTICAS_CONTAGEM + ESTATISTICAS_PERCENTUAIS]
        .notna()
        .sum()
        .to_dict(),
        "partidas": len(df),
    }


def adicionar_rotulos(ax, casas_decimais=1, sufixo=""):
    """Escreve o valor acima de cada barra."""
    for container in ax.containers:
        rotulos = []
        for valor in container.datavalues:
            if np.isnan(valor):
                rotulos.append("N/D")
            else:
                texto = f"{valor:.{casas_decimais}f}".replace(".", ",")
                rotulos.append(f"{texto}{sufixo}")
        ax.bar_label(container, labels=rotulos, padding=3, fontsize=9)


def configurar_eixo(ax, titulo: str, ylabel: str):
    ax.set_title(titulo, fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", linestyle="--", alpha=0.30)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plotar_comparativo(
    nomes: list[str], resumos: list[dict], arquivo_saida: Path
) -> None:
    figura, eixos = plt.subplots(3, 1, figsize=(12, 15))
    figura.suptitle(
        f"Comparativo das últimas partidas: {nomes[0]} x {nomes[1]}",
        fontsize=18,
        fontweight="bold",
        y=0.985,
    )

    largura = 0.36

    # Gráfico 1: quantidades de vitórias, empates e derrotas.
    categorias_resultado = ["Vitórias", "Empates", "Derrotas"]
    x = np.arange(len(categorias_resultado))
    for indice, (nome, resumo) in enumerate(zip(nomes, resumos)):
        valores = [resumo["resultados"][categoria] for categoria in categorias_resultado]
        eixos[0].bar(
            x + (indice - 0.5) * largura,
            valores,
            largura,
            label=nome,
            color=CORES[indice],
        )
    eixos[0].set_xticks(x, categorias_resultado)
    eixos[0].set_ylim(bottom=0)
    configurar_eixo(eixos[0], "Resultados", "Número de partidas")
    adicionar_rotulos(eixos[0], casas_decimais=0)
    eixos[0].legend(frameon=False)

    # Gráfico 2: estatísticas cuja unidade é quantidade por partida.
    nomes_curtos = ["Escanteios", "Gols", "Assistências", "Cartões\namarelos", "Cartões\nvermelhos"]
    x = np.arange(len(ESTATISTICAS_CONTAGEM))
    for indice, (nome, resumo) in enumerate(zip(nomes, resumos)):
        valores = [resumo["medias_contagem"][coluna] for coluna in ESTATISTICAS_CONTAGEM]
        eixos[1].bar(
            x + (indice - 0.5) * largura,
            valores,
            largura,
            label=nome,
            color=CORES[indice],
        )
    eixos[1].set_xticks(x, nomes_curtos)
    eixos[1].set_ylim(bottom=0)
    configurar_eixo(eixos[1], "Médias por partida", "Média")
    adicionar_rotulos(eixos[1])
    eixos[1].legend(frameon=False)

    # Gráfico 3: variáveis que já são percentuais.
    nomes_percentuais = ["Posse de bola", "Dribles bem-sucedidos"]
    x = np.arange(len(ESTATISTICAS_PERCENTUAIS))
    for indice, (nome, resumo) in enumerate(zip(nomes, resumos)):
        valores = [
            resumo["medias_percentuais"][coluna]
            for coluna in ESTATISTICAS_PERCENTUAIS
        ]
        eixos[2].bar(
            x + (indice - 0.5) * largura,
            valores,
            largura,
            label=nome,
            color=CORES[indice],
        )
    eixos[2].set_xticks(x, nomes_percentuais)
    eixos[2].set_ylim(0, 100)
    configurar_eixo(eixos[2], "Médias percentuais", "Percentual (%)")
    adicionar_rotulos(eixos[2], sufixo="%")
    eixos[2].legend(frameon=False)

    figura.text(
        0.5,
        0.012,
        "Valores ausentes são ignorados nas médias; confira a cobertura exibida no terminal.",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    figura.tight_layout(rect=[0.03, 0.03, 0.97, 0.965], h_pad=3)
    figura.savefig(arquivo_saida, dpi=300, bbox_inches="tight")
    print(f"Gráfico salvo em: {arquivo_saida.resolve()}")
    plt.show()


def exibir_cobertura(nomes: list[str], resumos: list[dict]) -> None:
    print("\nCobertura das estatísticas usadas nas médias:")
    for nome, resumo in zip(nomes, resumos):
        print(f"\n{nome} ({resumo['partidas']} partidas):")
        for coluna, quantidade in resumo["cobertura"].items():
            print(f"- {coluna}: {quantidade}/{resumo['partidas']} valores disponíveis")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compara resultados e médias estatísticas de dois times."
    )
    parser.add_argument("csv_time_1", type=Path, help="CSV do primeiro time")
    parser.add_argument("csv_time_2", type=Path, help="CSV do segundo time")
    parser.add_argument(
        "--saida",
        type=Path,
        default=Path("comparativo_times.png"),
        help="Imagem PNG gerada (padrão: comparativo_times.png)",
    )
    args = parser.parse_args()

    try:
        dataframes = [carregar_csv(args.csv_time_1), carregar_csv(args.csv_time_2)]
        nomes = [
            nome_do_time(dataframes[0], args.csv_time_1),
            nome_do_time(dataframes[1], args.csv_time_2),
        ]
        resumos = [
            resumir(dataframes[0], nomes[0]),
            resumir(dataframes[1], nomes[1]),
        ]
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as erro:
        parser.error(str(erro))

    exibir_cobertura(nomes, resumos)
    plotar_comparativo(nomes, resumos, args.saida)


if __name__ == "__main__":
    main()
