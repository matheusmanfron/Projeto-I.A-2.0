import pandas as pd

df = pd.read_csv('celtic_partidas_padronizadas.csv')

print("Contagem de resultados")
contagem_resultado = df['resultado'].value_counts()
print(contagem_resultado)

print("Contagem de adversários")
contagem_adversarios = df['adversario'].value_counts()
print(contagem_adversarios)

print("Estatisticas gerais de gols")
estatisticas_gols = df['Gols'].agg(['max', 'min', 'mean', 'median'])
print(estatisticas_gols)

print("Estatisticas gerias de escanteio")
estatisticas_escanteios = df['Escanteios'].agg(['max', 'min', 'mean', 'median'])
print(estatisticas_escanteios)

