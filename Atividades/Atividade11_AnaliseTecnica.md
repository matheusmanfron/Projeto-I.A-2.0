# Avaliação do modelo KNN e plano de melhorias para a etapa final

## 1. O que funcionou bem no modelo

### 1.1. Preparação de atributos com histórico anterior à partida

**O que funcionou:** o notebook constrói atributos de forma recente dos times usando médias móveis dos últimos 5 e 10 jogos (`pts_5`, `pts_10`), além de médias dos últimos 5 jogos para gols, escanteios, posse de bola e cartões. A função `media_movel` utiliza `shift(1)` antes da janela móvel, excluindo a partida atual do histórico usado para calcular as médias. O código também calcula a forma recente do adversário (`adv_pts_5`, `adv_pts_10`) e a diferença de pontos (`dif_pts_10`).

**Evidência:** a base original tinha **3.446 linhas e 17 colunas**. Após a criação dos atributos, **82 linhas foram removidas por falta de histórico**, restando **3.274 partidas/observações** para modelagem. As médias dos atributos calculados também foram inspecionadas com `describe()`.

**Por que é um acerto:** a forma recente é relevante para estimar o desempenho de uma equipe, e excluir a partida atual das médias reduz o risco de usar informação do próprio jogo para prever seu resultado.

**Como preservar:** manter o `shift(1)` na construção das médias móveis e documentar claramente quais estatísticas representam o time e quais representam o adversário. Na etapa final, verificar com testes que nenhuma feature de uma partida utiliza dados dessa própria partida ou de jogos futuros.

### 1.2. Divisão temporal e validação cruzada compatíveis com a previsão de jogos futuros

**O que funcionou:** o notebook ordena as observações por data e separa o conjunto de treino das partidas mais antigas e o teste das mais recentes. A busca de hiperparâmetros utiliza `TimeSeriesSplit`, em vez de uma divisão aleatória para a validação cruzada.

**Evidência:** o treino ficou com **2.620 observações até 07/12/2024**; o teste ficou com **654 observações entre 08/12/2024 e 17/05/2026**. A busca em grade selecionou `n_neighbors=75`, `p=2` (distância euclidiana) e `weights=uniform`, com acurácia média de validação cruzada de **0,532**.

**Por que é um acerto:** em uma aplicação que pretende prever partidas futuras, avaliar em um período posterior é mais realista do que misturar partidas antigas e recentes aleatoriamente. O `TimeSeriesSplit` também ajuda a avaliar configurações respeitando a ordem temporal.

**Como preservar:** manter uma avaliação cronológica e registrar as datas de corte. Na versão final, ajustar a regra de corte para que todas as partidas da mesma data fiquem no mesmo conjunto e confirmar que cada dobra da validação usa somente observações anteriores para treinar.

### 1.3. Comparação com baselines simples

**O que funcionou:** o KNN foi comparado a duas referências: prever sempre a classe mais frequente e uma regra simples baseada no mando de campo.

**Evidência no conjunto de teste:**

| Abordagem | Acurácia | F1 macro |
|---|---:|---:|
| Baseline: classe mais frequente | 0,405 | 0,192 |
| Baseline: mando de campo | 0,469 | 0,354 |
| KNN | **0,508** | **0,392** |

**Por que é um acerto:** a comparação mostra que o KNN supera as duas referências avaliadas: melhora de **3,9 pontos percentuais** de acurácia em relação à regra do mando e de **4,8 pontos percentuais** em F1 macro. Isso dá uma referência concreta para avaliar se as próximas alterações realmente ajudam.

**Como preservar:** manter os dois baselines em todas as experiências futuras e comparar as métricas no mesmo conjunto de teste. A melhora observada é promissora, mas não prova, por si só, que o modelo seja suficientemente confiável para uso real.

## 2. O que não funcionou ou permanece frágil

### 2.1. O modelo quase não identifica empates

**O que não funcionou:** a classe `empate` tem desempenho muito baixo no teste.

**Evidência:** o relatório de classificação mostra, para empates, **precisão 0,18, recall 0,01 e F1-score 0,02**, com **151** exemplos reais. Na matriz de confusão, somente **2 dos 151 empates** foram previstos como empate; 68 foram previstos como derrota e 81 como vitória.

**Consequência prática:** o modelo tende a transformar partidas equilibradas em previsões de vitória ou derrota. Como a saída pretendida é distinguir derrota, empate e vitória, esse problema limita bastante a utilidade das previsões.

**Quanto compromete a AS:** **alto**. A métrica geral pode parecer razoável, mas o modelo praticamente não reconhece uma das três classes.

### 2.2. O desempenho geral ainda é moderado e o F1 macro é baixo

**O que não funcionou:** apesar de superar os baselines, o KNN ainda erra em uma parcela expressiva das partidas e apresenta desempenho desigual entre as classes.

**Evidência:** no teste, a acurácia é **0,508** e o F1 macro é **0,392**. O F1 das classes derrota e vitória é **0,57** e **0,58**, respectivamente, enquanto o F1 do empate é **0,02**. A acurácia da validação cruzada usada para selecionar hiperparâmetros foi **0,532**, superior à acurácia final de teste, **0,508**.

**Consequência prática:** as previsões podem ser úteis como protótipo exploratório, mas não devem ser apresentadas como resultados certeiros. A diferença entre validação e teste também indica que a configuração escolhida não se transfere perfeitamente ao período posterior.

**Quanto compromete a AS:** **médio a alto**. O modelo tem um resultado melhor que as referências simples, mas ainda precisa de avaliação e melhoria antes de sustentar conclusões fortes.

### 2.3. A avaliação precisa garantir uma separação temporal rigorosa

**O que está frágil:** o corte é calculado por uma posição na lista de datas e depois aplicado com `data <= data_corte` para treino e `data > data_corte` para teste. Se várias observações compartilham a data de corte, o conjunto de treino pode ultrapassar a proporção nominal de 80%. Além disso, é importante auditar toda a construção dos atributos e a validação cruzada para assegurar que não haja informação futura.

**Evidência:** o notebook declara uma proporção de treino de **0,80**, mas usa uma data de corte obtida pelo índice de uma linha, não por um limite explícito entre datas únicas. O próprio código usa `shift(1)` para as médias móveis, o que é uma proteção positiva, mas a ausência de uma auditoria explícita de vazamento deixa uma verificação necessária.

**Consequência prática:** se a separação ou as features incorporarem informação futura, as métricas podem ficar artificialmente otimistas e não representar o desempenho em partidas ainda não disputadas.

**Quanto compromete a AS:** **alto se for encontrado vazamento**; no momento, é um risco metodológico a verificar, não uma prova de que o modelo esteja vazando dados.

## 3. Possíveis causas dos erros

### Problema A — Baixa identificação de empates

**Hipótese técnica principal:** os atributos atuais podem separar melhor equipes com desempenho recente forte ou fraco do que distinguir jogos que terminam empatados. As médias de pontos, gols, posse e escanteios descrevem a forma geral, mas podem não representar suficientemente a proximidade entre os times ou a probabilidade específica de empate.

**Evidência disponível:** o recall de empate é **0,01** e apenas **2 de 151** empates foram classificados corretamente. No treino, as classes não estão igualmente distribuídas: vitória **41,6%**, derrota **35,1%** e empate **23,3%**. Portanto, existe desbalanceamento moderado, mas a diferença de frequência sozinha não comprova a causa do problema.

**Outra hipótese a testar:** a distância usada pelo KNN e a configuração selecionada podem favorecer regiões ocupadas pelas classes derrota e vitória. O melhor modelo usa **75 vizinhos**, uma vizinhança relativamente ampla, que pode suavizar padrões específicos dos empates.

**Como verificar:** analisar a matriz de confusão e a distribuição de previsões; comparar `class_weight` não é uma opção direta no `KNeighborsClassifier`, então testar estratégias adequadas ao KNN, como ponderação por distância, diferentes valores de `n_neighbors` e avaliação por F1 macro e recall por classe. Comparar também com um modelo de referência que aceite pesos de classe, sem substituir a avaliação no mesmo período de teste.

### Problema B — Acurácia e F1 macro limitados

**Hipótese técnica principal:** as features disponíveis podem não conter informação suficiente para prever o resultado com precisão maior. A base inclui forma recente, gols, escanteios, posse, cartões e mando, mas não demonstra incluir fatores como força do elenco, escalação, lesões, descanso, importância da partida ou força do adversário ajustada por contexto.

**Evidência disponível:** a acurácia do KNN no teste é **0,508**, contra **0,469** no baseline de mando. O F1 macro é **0,392**, e o resultado da classe empate é muito inferior aos demais. Isso sustenta a conclusão de que o desempenho é limitado, mas não identifica sozinho qual feature falta.

**Hipóteses adicionais:** o KNN pode não ser o algoritmo mais adequado para a relação entre as estatísticas e o resultado; a escala dos atributos também importa para um algoritmo baseado em distância. O notebook já utiliza `StandardScaler` em um `Pipeline`, o que é um ponto positivo, e faz busca de hiperparâmetros, mas somente entre configurações do KNN.

**Como verificar:** comparar KNN com pelo menos um modelo alternativo, como regressão logística multinomial ou árvore/Random Forest, mantendo os mesmos atributos, divisão temporal e métricas. Avaliar a contribuição de grupos de features por ablação, retirando um grupo de cada vez e observando se F1 macro e recall de empate mudam.

### Problema C — Possível risco na avaliação temporal

**Hipótese técnica:** o corte por data pode gerar um tamanho de treino diferente dos 80% pretendidos devido a várias observações na mesma data. Também é necessário confirmar que todas as médias históricas são calculadas somente com jogos anteriores à partida prevista e que as dobras do `TimeSeriesSplit` não compartilham informação futura por meio de features pré-calculadas.

**Evidência disponível:** o notebook ordena por data, usa `shift(1)` nas médias móveis e emprega `TimeSeriesSplit`; essas escolhas reduzem o risco. Porém, o corte é feito a partir do índice de uma linha e a auditoria não apresenta uma checagem específica de vazamento por data/partida. Assim, a hipótese permanece uma verificação pendente, não um erro comprovado.

**Como verificar:** dividir com base em datas únicas; testar se a data máxima do treino é anterior à data mínima do teste; revisar o cálculo de cada feature por equipe e adversário; e garantir que as médias móveis usem apenas partidas anteriores. Reexecutar a avaliação depois da auditoria e comparar as métricas.

## 4. Melhorias definidas para a etapa final

| Problema | Ação concreta | Por que pode ajudar | Quando |
|---|---|---|---|
| Baixo recall de empate | Testar `weights="distance"` e uma grade mais ampla de `n_neighbors`; escolher configurações usando F1 macro e recall por classe, além da acurácia. | Pode reduzir a influência de vizinhos distantes e evitar selecionar um modelo que favoreça somente as classes mais fáceis. | **Antes do próximo encontro:** primeira rodada de experimentos. |
| Baixo desempenho geral | Comparar KNN com regressão logística multinomial e Random Forest, usando as mesmas features e o mesmo corte temporal. | Mostra se o limite vem da configuração do KNN ou se outros modelos aprendem melhor os padrões presentes na base. | **Próxima etapa de desenvolvimento:** implementar e comparar modelos. |
| Features talvez insuficientes | Fazer ablação por grupos: forma em pontos, estatísticas de gols/posse/escanteios/cartões e mando. Registrar o F1 macro e o recall de empate de cada variante. | Identifica quais grupos de atributos contribuem de fato e quais acrescentam pouco ou ruído. | **Depois da comparação de modelos:** antes de congelar as features finais. |
| Possível risco temporal | Refazer a separação usando datas únicas; verificar a ordem temporal em cada dobra; auditar se cada média histórica exclui a partida atual e jogos futuros. | Evita uma estimativa artificialmente otimista e torna o teste mais parecido com o uso real. | **Imediatamente, antes de novos resultados serem considerados definitivos.** |
| Desbalanceamento moderado | Registrar a distribuição das classes no treino e no teste; testar estratégias de tratamento apenas no treino e medir o efeito por classe. | Ajuda a avaliar se o desbalanceamento contribui para a omissão dos empates, sem alterar indevidamente o conjunto de teste. | **Na mesma rodada dos experimentos de empate.** |
| Risco de interpretar a acurácia isoladamente | Manter acurácia, F1 macro, precision/recall/F1 por classe e matriz de confusão nos resultados finais. | Impede que uma métrica agregada esconda a falha na classe empate. | **Em todas as avaliações e na apresentação final.** |

### Critérios para considerar uma melhoria válida

Uma alteração será considerada útil se for avaliada no mesmo conjunto de teste cronológico e apresentar melhora consistente em **F1 macro** e/ou **recall de empate**, sem queda desproporcional nas demais classes. A acurácia será mantida para comparação com os baselines, mas não será usada sozinha para escolher o modelo.

O conjunto de teste não deve ser usado repetidamente para escolher hiperparâmetros. As decisões devem ser tomadas com validação temporal dentro do treino; o teste final fica reservado para a avaliação da configuração selecionada.

## 5. Síntese para a etapa final

O protótipo já apresenta três acertos concretos: cálculo de forma recente sem incluir a partida atual, avaliação cronológica com `TimeSeriesSplit` e comparação com baselines. No teste, o KNN alcançou **0,508 de acurácia e 0,392 de F1 macro**, superando as duas referências simples.

A principal fragilidade é a classe **empate**, com recall de **0,01** e F1 de **0,02**. A prioridade é investigar essa falha, comparar modelos e atributos, e auditar a separação temporal antes de tratar as métricas como definitivas. As hipóteses sobre insuficiência de atributos, efeito dos hiperparâmetros e vazamento temporal devem ser testadas; não são apresentadas como causas comprovadas.
