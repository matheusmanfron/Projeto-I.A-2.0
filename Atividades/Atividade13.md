# Comparação entre rede neural e KNN na previsão de resultados de futebol

## 1. Experimento executado

Foi treinada uma rede neural utilizando o algoritmo `MLPClassifier`, com duas camadas escondidas, contendo 32 e 16 neurônios, respectivamente. A função de ativação utilizada foi ReLU, com otimizador Adam, limite de 500 épocas e semente aleatória 42.

As variáveis numéricas foram padronizadas utilizando `StandardScaler`. Foram utilizadas 11 características históricas das equipes e de seus adversários.

## 2. Comparação com o modelo clássico

A rede neural foi comparada ao KNN, já utilizado anteriormente no projeto, e a um baseline que sempre prevê a classe mais frequente.

Os modelos utilizaram os mesmos dados, com divisão cronológica de 2.686 registros para treinamento e 670 para teste.

O baseline apresentou acurácia de 40,3%, o KNN alcançou 50,0% e a rede neural obteve 47,0%.

## 3. Análise dos resultados

A rede neural apresentou uma acurácia 3 pontos percentuais inferior à do KNN. Entretanto, seu F1 macro foi ligeiramente superior, alcançando 0,421 contra 0,411 do KNN.

Uma hipótese para esse resultado é que o conjunto de dados tabulares possui uma quantidade limitada de informações para o ajuste dos parâmetros da rede neural. Além disso, a dificuldade de identificar empates continua afetando os dois modelos.

## 4. Comparação entre treino e teste

A rede neural apresentou 65,0% de acurácia nos dados de treinamento e 47,0% nos dados de teste.

Essa diferença de 18 pontos percentuais sugere *overfitting*, indicando que o modelo aprendeu características dos dados de treinamento que não conseguiu generalizar adequadamente para partidas mais recentes.

## 5. Decisão sobre o projeto final

Com base neste experimento, decidimos manter o KNN como modelo principal do projeto, pois apresentou melhor acurácia no conjunto de teste e uma diferença menor entre treinamento e teste.

A rede neural demonstrou potencial para melhorar a identificação de empates, mas ainda necessita de ajustes e novos experimentos antes de justificar sua utilização como modelo principal.

## 6. Dificuldades técnicas

Durante o treinamento da rede neural, ocorreu um `ConvergenceWarning`, indicando que o algoritmo atingiu o limite de 500 épocas sem alcançar o critério de convergência.

Para auxiliar no treinamento, foi utilizada a padronização das variáveis com `StandardScaler`. O aviso foi registrado, mas não completamente resolvido. Como possíveis melhorias futuras, podem ser testados outros números de neurônios, taxas de aprendizado e limites de épocas.

O experimento também evidenciou a dificuldade de generalização da rede neural, observada pela diferença entre os resultados de treinamento e teste.
