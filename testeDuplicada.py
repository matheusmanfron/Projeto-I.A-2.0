import pandas as pd

df = pd.read_csv('celtic_partidas_estatisticas_nomeadas.csv')

contagem_resultado = df['resultado'].value_counts()
print(contagem_resultado)

contagem_adversarios = df['adversario'].value_counts()
print(contagem_adversarios)

estatisticas_gols = df['Gols'].agg(['max', 'min', 'mean', 'median'])
print(estatisticas_gols)