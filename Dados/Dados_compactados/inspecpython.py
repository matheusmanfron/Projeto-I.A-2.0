import pandas as pd

df = pd.read_csv("Partidas_Compactadas.csv")

df.shape #(linhas, colunas) - tamanho da base
print("Tamanho da base")

df.head() # primeiras 5 linhas
print("Primeiras linhas")

df.info() # tipos de dados e valores não nulos por coluna
print("Tipos de dados")

df.describe(include="object") # resumo das colunas de text
print("Resumo colunas de texto")

df.isnull().sum() # quantidade de valores ausentes por coluna
print("Quantidade de valores nulos")

df.duplicated().sum() # número de linhas duplicadas
print("Linhas duplicadas")

df["Gols"].unique() # categorias únicas de uma coluna

#Proporção de cada classe na coluna alvo (diagnóstico de desequilíbrio)

df["Gols"].value_counts(normalize=True)