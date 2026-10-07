# Transformações necessárias no dataset
    *Padronizei os tipos de dados pois o pandas pode falhar na hora de computar
    algum dado erroniamente tipado, por exemplo, deixar os textos em string, datas em date.

    *Tratei os dados nulos de forma diferente para cada contexto dos dados, como as
    estatisticas não eram registradas no período antes de 2017, retirei essas no data set,
    Para cartões amaerelos e vermelhos e gols, preenchi os campos vazios com 0, pois, no caso de gols, os vazios apareciam mais em empates e derrotas (mais provável da equipe observada
    não marcar gols), e para os cartões fiz o mesmo tratamento pois nem todas as partidas tem
    cartões. Em assistências e dribles bem sucedidos, eliminei as colunas pois havia muitos dados
    vazios ou nulos, sendo inviável popular esses dados artificalmente por médias.

# Registro de decisões:
    Colunas afetadas |    Mudança        |                  Justificativa
    Gols             | Preenchido com 0  |  Pois só não eram registrados em empates e derrotas
    Cartões          | Preenchido com 0  |  Mais provável uma partida sem amarelos e vermelhos  
    Dribles          | Retirado          |  Pois essa estatistica só aparecia a partir de 2022
    Assitências      | Retirado          | Pois mais de 50% dos dados estavam em falta

# Registros
    *Na pasta de dados compactados, está o arquivo CSV Partidas_Tratadas.csv, e o código Python
    feito no colab está na pasta ScriptsPython com o nome de Tratamento_base.ipynb.