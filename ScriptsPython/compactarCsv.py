from pathlib import Path
import pandas as pd

PASTA_CSVS = Path(r"C:\Users\Windows\Documents\projetoI.A\Dados\Dados_Brutos")
ARQUIVO_SAIDA = PASTA_CSVS / "Partidas_Compactadas.csv"

arquivos_csv = [
    arquivo
    for arquivo in PASTA_CSVS.glob("*.csv")
    if arquivo.name != ARQUIVO_SAIDA.name
]

if not arquivos_csv:
    raise FileNotFoundError("Nenhum CSV encontrado")

dataframes = []

for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo, encoding="utf-8-sig")
    dataframes.append(df)

base_completa = pd.concat(dataframes, ignore_index=True)

base_completa.to_csv(
    ARQUIVO_SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print(f"Arquivo criado: {ARQUIVO_SAIDA}")
print(f"Quantidade de arquivos unidos: {len(arquivos_csv)}")
print(f"Quantidade total de linhas: {len(base_completa)}")