import pandas as pd

df = pd.read_csv("Partidas_Compactadas.csv")

print("Tamanho da base")
df.shape #(linhas, colunas) - tamanho da base

print("Primeiras linhas")
df.head() # primeiras 5 linhas

print("Tipos de dados")
df.info() # tipos de dados e valores não nulos por coluna

print("Resumo colunas de texto")
df.describe(include="object") # resumo das colunas de text

print("Quantidade de valors nulos")
df.isnull().sum() # quantidade de valores ausentes por coluna

print("Linhas duplicadas")
df.duplicated().sum() # número de linhas duplicadas

df["Gols"].unique() # categorias únicas de uma coluna

#Proporção de cada classe na coluna alvo (diagnóstico de desequilíbrio)

df["Gols"].value_counts(normalize=True)