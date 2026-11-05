# Análise de Aplicações Semelhantes
# --Forebet

# 1.Aplicação escolhida e contexto
    Aplicação: Forebet, Mathematical Football Predictions
    Desenvolvedor: Forebet / Forecreations
    Link: https://www.forebet.com/

    O Forebet é uma plataforma de análise estatística e previsão de resultados esportivos, com destaque para o futebol. Seu objetivo é utilizar dados históricos das equipes para calcular probabilidades de resultados futuros, como vitória do mandante, empate ou vitória do visitante. Além disso, apresenta estimativas de placares, quantidade de gols e outras estatísticas. A plataforma é voltada principalmente para torcedores e pessoas interessadas em análises esportivas baseadas em dados.

# 2.Dados de entrada
    O Forebet utiliza dados históricos de partidas e estatísticas das equipes para realizar suas previsões. Entre as informações consideradas estão os resultados anteriores, gols marcados e sofridos, desempenho recente, confrontos diretos entre as equipes, desempenho como mandante ou visitante e tendências ao longo das temporadas.

# 3.Saída produzida
    A principal saída do Forebet é uma previsão probabilística dos resultados de uma partida.

    O sistema apresenta três probabilidades: vitória do mandante (1), empate (X) e vitória do visitante (2). Também pode apresentar o placar previsto, a média estimada de gols e outras previsões estatísticas.

    Esses resultados são exibidos em tabelas e páginas específicas das partidas, permitindo que o usuário compare os cenários.

# 4.Técnica provável, com justificativa
    A técnica mais provável é uma combinação de modelos estatísticos preditivos e aprendizado de máquina supervisionado.

    Essa hipótese se justifica porque o sistema utiliza características de partidas anteriores para estimar resultados futuros. Os dados históricos possuem resultados conhecidos, que podem ser utilizados para ajustar e avaliar modelos preditivos.

    A previsão de vitória, empate ou derrota pode ser tratada como um problema de classificação multiclasse, enquanto a estimativa da quantidade de gols pode envolver técnicas de regressão e modelos probabilísticos.

    A própria plataforma informa que utiliza algoritmos matemáticos, modelos estatísticos e técnicas de aprendizado de máquina.

# 5.Riscos, limitações e impactos
    Um dos principais riscos é a previsão incorreta de um resultado. Por exemplo, o sistema pode indicar uma vitória como o cenário mais provável, mas a partida terminar empatada. Em uma classificação multiclasse, tanto falsos positivos quanto falsos negativos podem ocorrer para cada resultado. O custo desses erros depende da utilização da previsão.

    Outro risco é o viés causado pela disponibilidade desigual de dados. Equipes e campeonatos com poucos registros históricos podem apresentar previsões menos confiáveis do que competições com estatísticas mais completas. Isso pode prejudicar principalmente a análise de clubes menos conhecidos.

    Também existem limitações de explicabilidade. Embora o Forebet apresente probabilidades e estatísticas, o usuário não necessariamente consegue identificar o peso exato de cada variável ou compreender como o algoritmo chegou ao resultado final.

# 6.Conexão com o projeto Fut Analitcs
    O Forebet possui uma relação direta com o Fut Analitics, desenvolvido no projeto semestral. Ambos procuram utilizar estatísticas históricas de futebol para prever resultados de partidas.

    No Fut Analitics, utilizo dados do Campeonato Escocês e experimento algoritmos de aprendizado supervisionado, como KNN e MLPClassifier, para classificar os resultados em vitória, empate ou derrota.

    Uma decisão técnica interessante do Forebet é apresentar as probabilidades dos três resultados possíveis, em vez de fornecer somente uma previsão definitiva. Essa abordagem também faz parte dos objetivos do Fut Analitics e pode tornar a apresentação das previsões mais informativa.

    Uma limitação compartilhada é a dependência da qualidade e da quantidade dos dados históricos. Caso as estatísticas estejam incompletas ou não representem adequadamente o desempenho atual das equipes, as previsões podem perder qualidade.

    Um erro que queremos evitar é apresentar uma previsão como se fosse uma certeza. Para isso, pretendemos utilizar probabilidades, comparar diferentes métricas de desempenho e deixar claras as limitações do modelo.

