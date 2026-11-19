# Atividade 15 — Relatório Final do Projeto Fut Analitics

**Projeto:** Fut Analitics  
**Tema:** Previsão de resultados de partidas de futebol utilizando aprendizado de máquina  
**Repositório:** https://github.com/matheusmanfron/Projeto-I.A-2.0

## 1. Principais resultados obtidos

O Fut Analitics tem como objetivo prever resultados de partidas de futebol utilizando estatísticas históricas das equipes. O problema foi tratado como uma classificação supervisionada de três resultados: derrota, empate e vitória.

A base foi construída com dados da liga escocesa de futebol, obtidos pela API SportMonks. Inicialmente, foram reunidos 3.446 registros. Após a preparação dos atributos históricos e a remoção dos registros sem histórico suficiente, restaram 3.356 observações para o experimento principal, sendo 2.686 utilizadas no treinamento e 670 no teste.

O modelo principal escolhido foi o KNN (*K-Nearest Neighbors*), utilizando 35 vizinhos, distância euclidiana e padronização dos atributos com `StandardScaler`.

### 1.1. Acurácia

| Modelo | Acurácia no teste |
|---|---:|
| Baseline — classe mais frequente | 40,3% |
| Baseline — mando de campo | 46,7% |
| KNN | **50,0%** |
| Rede neural MLP | 47,0% |

O KNN apresentou uma melhora de 9,7 pontos percentuais em relação ao baseline da classe mais frequente e de 3,3 pontos percentuais em relação à regra baseada no mando de campo.

**Interpretação:** o modelo acertou 335 das 670 previsões avaliadas. Isso significa que conseguiu identificar padrões úteis nas estatísticas das equipes, mas ainda errou aproximadamente metade dos resultados.

### 1.2. F1-score macro

| Modelo | F1 macro |
|---|---:|
| Baseline — classe mais frequente | 0,191 |
| Baseline — mando de campo | 0,353 |
| KNN | **0,411** |
| Rede neural MLP | 0,421 |

O F1 macro foi escolhido como uma das principais métricas porque considera o desempenho das três classes de maneira equilibrada.

**Interpretação:** embora o KNN apresente um resultado superior aos baselines, sua capacidade de reconhecer vitórias, empates e derrotas ainda é desigual. A rede neural apresentou F1 macro ligeiramente superior, mas não superou o KNN em acurácia.

### 1.3. Identificação de empates

O principal problema encontrado foi a dificuldade de prever empates.

No conjunto de teste, ocorreram 157 empates reais, mas o KNN identificou corretamente apenas 9, resultando em um recall de aproximadamente 5,7%. Os dois baselines avaliados não identificaram nenhum empate.

**Interpretação:** a cada 100 empates reais, o modelo conseguiria reconhecer aproximadamente 6. Isso significa que a maioria das partidas que terminam empatadas acaba sendo classificada como vitória ou derrota.

### 1.4. Comparação com redes neurais

Também foi realizado um experimento com `MLPClassifier`, utilizando duas camadas ocultas de 32 e 16 neurônios.

A rede neural apresentou 65% de acurácia no treinamento e 47% no teste, uma diferença de 18 pontos percentuais, sugerindo *overfitting*.

Diante desses resultados, o KNN foi mantido como modelo principal, pois apresentou maior acurácia no teste e uma diferença menor entre os resultados de treinamento e teste.

## 2. Limitações do modelo

### 2.1. Dificuldade na previsão de empates

O modelo apresenta um desempenho muito inferior na classe empate, identificando corretamente apenas 9 de 157 ocorrências.

**Impacto prático:** uma partida equilibrada pode ser apresentada como provável vitória de uma das equipes, reduzindo a confiabilidade das previsões.

### 2.2. Restrição da base de dados

Os dados utilizados são provenientes da liga escocesa masculina e representam um conjunto específico de equipes e temporadas.

**Impacto prático:** não é possível garantir que o modelo apresente desempenho semelhante em outras ligas, como o Campeonato Brasileiro ou a Premier League inglesa, sem novos treinamentos e avaliações.

### 2.3. Ausência de variáveis importantes

O modelo utiliza estatísticas históricas, como gols, posse de bola, escanteios, cartões, mando de campo e desempenho recente. Entretanto, não incorpora diretamente informações como escalações confirmadas, lesões, suspensões e condições físicas dos jogadores.

**Impacto prático:** o modelo pode considerar uma equipe favorita com base no histórico, mesmo quando ela apresenta desfalques importantes na partida prevista.

### 2.4. Desempenho geral limitado

Apesar de superar os baselines, a acurácia de 50% ainda é insuficiente para considerar o modelo altamente confiável.

**Impacto prático:** o sistema pode auxiliar na análise estatística de uma partida, mas não deve ser utilizado como única fonte para decisões que dependam do resultado.

## 3. Possíveis vieses identificados

### 3.1. Representatividade dos dados

A base representa partidas da liga escocesa masculina. Equipes de outras competições, categorias femininas e divisões inferiores não estão representadas no conjunto utilizado.

Isso gera um possível viés de representatividade, pois o modelo aprende padrões específicos das equipes e do campeonato analisado.

### 3.2. Variáveis que podem funcionar como proxy

O mando de campo e o desempenho histórico podem funcionar como indicadores indiretos da força e das condições competitivas de uma equipe.

Por exemplo, equipes com melhores estruturas e elencos podem apresentar resultados históricos superiores, influenciando as previsões.

Não foram identificadas variáveis pessoais sensíveis, como raça, religião ou gênero dos jogadores, entre os atributos utilizados. Entretanto, isso não elimina possíveis vieses esportivos presentes nos dados.

### 3.3. Diferenças de desempenho entre subgrupos

Foi possível analisar o desempenho por classe de resultado:

| Resultado | Recall |
|---|---:|
| Derrota | 62% |
| Empate | 5,7% |
| Vitória | 65% |

Os resultados mostram uma diferença significativa entre as classes. O modelo identifica a maioria das vitórias e derrotas, mas quase não reconhece empates.

Essa é uma evidência concreta de desempenho desigual entre os grupos de resultados.

Ainda não foi realizada uma avaliação separada por equipe, temporada ou condição de mandante e visitante. Portanto, não é possível afirmar se o modelo apresenta o mesmo desempenho para todos os clubes.

### 3.4. Possíveis vieses históricos

Os dados registram resultados reais de partidas, e não decisões humanas de aprovação ou rejeição, como acontece em sistemas de crédito ou seleção profissional.

Por isso, o risco de reproduzir diretamente decisões humanas discriminatórias é menor nesse contexto. Entretanto, os resultados históricos refletem diferenças competitivas entre equipes, além de possíveis diferenças na cobertura e na qualidade das estatísticas coletadas.

## 4. Riscos de uso indevido

**Classificação do risco: baixo no contexto educacional previsto, podendo chegar a alto em situações de uso financeiro.**

O Fut Analitics foi desenvolvido como um projeto acadêmico de análise e previsão esportiva. Nesse contexto, uma previsão incorreta não impede o acesso a direitos ou serviços e normalmente possui consequências limitadas.

Entretanto, existe risco de uso indevido caso alguém interprete as previsões como garantias de resultados e as utilize para realizar apostas esportivas.

### Custo de um erro

Um falso positivo de vitória ocorre quando o modelo prevê que uma equipe vencerá, mas ela empata ou perde.

Nesse caso, o usuário recebe uma previsão incorreta. Se utilizar a informação apenas para análise esportiva, o impacto é pequeno. Caso utilize a previsão para apostar dinheiro, poderá sofrer prejuízo financeiro.

O custo do erro é assumido principalmente por quem utiliza a previsão.

### Possibilidade de contestação

O usuário pode comparar a previsão com o resultado real e consultar as métricas de avaliação do modelo. Entretanto, o projeto ainda não possui um mecanismo específico para contestação ou explicação individual de cada previsão.

### Cenário de uso indevido

Um exemplo seria utilizar as probabilidades produzidas pelo Fut Analitics como recomendações de apostas, ignorando que o modelo acerta aproximadamente metade dos resultados e possui grande dificuldade para identificar empates.

Para reduzir esse risco, as previsões devem ser apresentadas como estimativas estatísticas, acompanhadas de informações sobre o desempenho e as limitações do modelo.

## 5. Melhorias futuras

### 5.1. Melhorar a identificação de empates

**Problema:** o KNN apresenta recall de apenas 5,7% para empates.

**Melhoria proposta:** testar diferentes quantidades de vizinhos, ponderação por distância e atributos que representem o equilíbrio entre as equipes, como diferenças absolutas entre suas médias históricas.

**Resultado esperado:** aumentar a identificação de empates sem prejudicar excessivamente as previsões de vitórias e derrotas.

### 5.2. Ampliar as informações utilizadas

**Problema:** as estatísticas atuais não representam todos os fatores que influenciam uma partida.

**Melhoria proposta:** incorporar dados disponíveis antes do jogo, como dias de descanso, desempenho como mandante ou visitante, lesões e escalações confirmadas.

**Resultado esperado:** permitir que o modelo considere situações que não são representadas apenas pelas médias históricas.

### 5.3. Comparar novos algoritmos

**Problema:** o KNN pode não ser o algoritmo mais adequado para os padrões presentes na base.

**Melhoria proposta:** comparar o modelo atual com regressão logística, Random Forest e outras configurações de redes neurais, utilizando a mesma divisão temporal e métricas.

**Resultado esperado:** identificar uma abordagem com melhor capacidade de generalização e desempenho mais equilibrado entre as três classes.

### 5.4. Avaliar o desempenho por equipe e temporada

**Problema:** a avaliação atual não demonstra se o modelo funciona igualmente bem para diferentes clubes e períodos.

**Melhoria proposta:** calcular acurácia e F1 macro separadamente por equipe, temporada e condição de mando de campo.

**Resultado esperado:** identificar possíveis diferenças de desempenho que não aparecem nas métricas gerais.

### 5.5. Melhorar a apresentação das previsões

**Problema:** uma classificação isolada pode transmitir mais certeza do que os resultados justificam.

**Melhoria proposta:** apresentar probabilidades para vitória, empate e derrota, verificar sua calibração e incluir informações sobre a confiabilidade histórica do modelo.

**Resultado esperado:** permitir uma interpretação mais adequada das previsões pelos usuários.

## 6. Estrutura da apresentação da AS

A apresentação final terá aproximadamente 8 minutos, seguida de até 4 minutos para perguntas.

| Etapa | Conteúdo | Tempo |
|---|---|---:|
| 1. Introdução | Apresentação do Fut Analitics e problema escolhido | 0:45 |
| 2. Dados utilizados | Fonte SportMonks, liga escocesa e preparação da base | 1:00 |
| 3. Metodologia | Aprendizado supervisionado, atributos históricos e KNN | 1:15 |
| 4. Resultados | Acurácia, F1 macro, baselines e matriz de confusão | 1:45 |
| 5. Comparação de modelos | KNN versus rede neural MLP | 0:45 |
| 6. Limitações e riscos | Dificuldade dos empates, vieses e uso indevido | 1:15 |
| 7. Melhorias e conclusão | Próximos passos e aprendizados do projeto | 1:15 |
| **Total** | | **8:00** |

Após a apresentação, serão reservados até 4 minutos para responder às perguntas sobre os resultados, as escolhas técnicas e as limitações do projeto.

## Conclusão

O Fut Analitics permitiu aplicar as principais etapas de um projeto de aprendizado de máquina, desde a coleta e preparação dos dados até o treinamento, a comparação e a avaliação de modelos.

O KNN conseguiu superar os modelos de referência, alcançando 50% de acurácia e F1 macro de 0,411. Entretanto, a análise mostrou que o desempenho ainda é limitado, especialmente na identificação de empates.

A comparação com redes neurais também demonstrou que utilizar um modelo mais complexo não garante melhores resultados.

Assim, o principal resultado do projeto não foi desenvolver um sistema capaz de prever partidas com alta confiabilidade, mas construir e avaliar um modelo funcional, identificar suas limitações e estabelecer melhorias fundamentadas em evidências.

O projeto permanece como um protótipo acadêmico de previsão esportiva, com possibilidades de evolução por meio de novos atributos, algoritmos e avaliações.
