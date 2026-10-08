🤖 Fut Analitics — Avaliação do Modelo (AP2)

Modelo: KNN (K-Nearest Neighbors) · Notebook: ModeloKNN.ipynb · Dados: Partidas_Tratadas.csv (Scottish Premiership, via SportMonks) Problema: classificação do resultado da partida, do ponto de vista de um time: derrota / empate / vitória. Cada linha da base é um time em uma partida (mando = 1 se joga em casa).

ℹ️ Origem dos números. Todos os valores abaixo foram obtidos executando o código do ModeloKNN.ipynb sobre o Partidas_Tratadas.csv (3.446 linhas; 3.356 após remover 90 sem histórico; treino de 2.686 linhas até 2024-12-04; teste de 670 linhas, de 2024-12-07 a 2026-05-17).

Configuração final do modelo: StandardScaler + KNeighborsClassifier(n_neighbors=35, p=2, weights="uniform"), escolhido por GridSearchCV com TimeSeriesSplit(5) apenas no treino. Atributos (11): mando, pts_5, pts_10, gols_5, escanteios_5, posse_5, amarelos_5, vermelhos_5, adv_pts_5, adv_pts_10, dif_pts_10.

1. Métricas (classificação)

Como é classificação, as métricas são acurácia, precisão, recall e F1, geradas pelo classification_report.

python
from sklearn.metrics import classification_report, accuracy_score

y_pred = modelo.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, digits=3))
Classe	Precisão	Recall	F1-score	Suporte
Derrota	0,51	0,62	0,56	243
Empate	0,20	0,06	0,09	157
Vitória	0,54	0,65	0,59	270
Acurácia			0,50 (0,500)	670
Macro avg	0,41	0,44	0,41 (0,411)	670

Leitura: o modelo acerta razoavelmente vitória (F1 0,59) e derrota (F1 0,56), com recall de 65% e 62%, mas quase não prevê empate: só 45 das 670 previsões foram "empate" e apenas 9 acertaram (recall de 5,7% sobre 157 empates reais). Isso é típico do futebol, em que o empate é a classe menos frequente (23% do teste) e a mais "no meio do caminho" entre dois times parecidos, e o KNN com k=35 acaba votando quase sempre em uma das duas classes maiores. A acurácia de 0,500 só é razoável porque derrota e vitória carregam o resultado; o F1 macro (0,411) mostra o custo de ignorar o empate.

2. Matriz de confusão
python
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, cmap="Blues", xticks_rotation=20
)
plt.title("Matriz de confusão — KNN (teste)")
plt.show()

Mostrar Imagem

Real \ Previsto	Derrota	Empate	Vitória	Total real
Derrota	151	22	70	243
Empate	66	9	82	157
Vitória	81	14	175	270
Total previsto	298	45	327	670

Como interpretar (a diagonal principal são os acertos; fora dela, os erros):

Linhas = resultado real; colunas = previsão do modelo. Acertos: 151 + 9 + 175 = 335 de 670 (50,0%).
Maior erro identificado: empates reais previstos como vitória (82 casos), seguido de vitórias reais previstas como derrota (81) e derrotas reais previstas como vitória (70). Somando, 148 dos 157 empates reais (94%) foram "empurrados" para vitória (82) ou derrota (66).
Confusão típica do futebol: o modelo troca vitória por derrota (e vice-versa) em 151 jogos (81 + 70), o que indica que os atributos de forma recente (pontos, gols, posse) separam o resultado de forma só parcial. Já o empate some porque não existe um perfil de atributos que o isole: jogos de times equilibrados caem no meio da distribuição e os vizinhos votam em vitória ou derrota.
Conclusão: o modelo captura uma tendência (time em boa forma e jogando em casa tende a vencer), mas os atributos usados não trazem informação suficiente para separar os três resultados, principalmente o empate.
3. Comparação com o baseline (Atividade 9)
python
from sklearn.dummy import DummyClassifier

baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
yb = baseline.predict(X_test)
# Use o MESMO baseline e a MESMA divisão da Atividade 9.

O notebook compara o KNN com dois baselines, na mesma divisão temporal do teste (670 linhas):

Métrica (teste)	Baseline: classe mais frequente	Baseline: mando (casa vence, fora perde)	KNN (meu modelo)	Dif. KNN vs. mais frequente	Dif. KNN vs. mando
Acurácia	0,403	0,467	0,500	+0,097 (+9,7 p.p.)	+0,033 (+3,3 p.p.)
F1 macro	0,191	0,353	0,411	+0,220	+0,058
Recall do empate	0,00	0,00	0,057	+0,057	+0,057

Veredito explícito: o KNN SUPERA os dois baselines em acurácia e F1 macro: por 9,7 pontos percentuais de acurácia e 0,220 de F1 macro sobre a classe mais frequente, e por 3,3 pontos percentuais de acurácia e 0,058 de F1 macro sobre o baseline do mando.

Ressalva estatística: com 670 linhas de teste, a margem de erro da acurácia é de cerca de ±3,8 p.p. (95%). O ganho sobre a classe mais frequente (9,7 p.p.) é claro. O ganho de acurácia sobre o baseline do mando (3,3 p.p.) é menor que essa margem, então deve ser apresentado como melhora modesta, e não como vitória decisiva; o ganho no F1 macro (0,058) é mais expressivo, porque vem principalmente de o KNN prever alguns empates. Além disso, 610 das 670 linhas do teste vêm de partidas que aparecem duas vezes (uma por time), o que reduz o tamanho efetivo da amostra.

4. Significado dos erros no domínio

Em um problema de 3 classes, falso positivo e falso negativo existem para cada classe. Na linguagem do futebol, usando "vitória" (do time analisado) como exemplo:

Falso positivo (alarme falso): o Fut Analitics diz "o time vai ganhar", mas o jogo termina em empate ou derrota. Foram 152 casos (70 derrotas + 82 empates), ou seja, 46% das previsões de vitória estavam erradas. Quem confiou na previsão se prepara para um cenário que não aconteceu.
Falso negativo (deixar passar): o time ganha, mas o modelo previu empate ou derrota. Foram 95 casos (81 + 14). O usuário descarta uma vitória que ia acontecer.

Para as outras classes (números do teste):

Classe	Falso positivo significa	Falso negativo significa
Derrota	Previu derrota, e o time empatou ou venceu (147 casos: 66 + 81)	O time perdeu e o modelo previu empate ou vitória (92 casos: 22 + 70)
Empate	Previu igualdade, e um time venceu (36 casos: 22 + 14)	Houve empate e o modelo não viu (148 casos, o erro mais comum do modelo)
Vitória	Previu vitória, e o time empatou ou perdeu (152 casos)	O time venceu e o modelo previu empate ou derrota (95 casos)
5. Métrica principal e justificativa

Métrica principal: F1-score macro (média do F1 das três classes). Valor atual: 0,411.

Por quê:

A acurácia engana. As classes são desbalanceadas (no teste: vitória 40,3%, derrota 36,3%, empate 23,4%), e um modelo que ignora o empate ainda parece bom: o KNN tem acurácia de 0,500, mas F1 do empate de 0,09. O F1 macro dá o mesmo peso às três classes e expõe esse problema.
Custo do erro. O Fut Analitics entrega probabilidades que o usuário usa para decidir. Aqui o alarme falso é mais caro: uma previsão confiante e errada gera falsa segurança. Já deixar passar um resultado apenas torna a previsão menos útil, sem induzir uma decisão errada.
Por isso acompanho a precisão das classes de vitória e derrota (0,54 e 0,51) como métrica secundária, e o F1 macro para vigiar o empate. O resultado atual mostra que o modelo ainda não cumpre bem esse segundo papel: o F1 macro só chegou a 0,411 porque o F1 do empate é muito baixo.

6. Teste de overfitting
python
from sklearn.metrics import accuracy_score, f1_score

for nome, X, y in [("treino", X_train, y_train), ("teste", X_test, y_test)]:
    p = modelo.predict(X)
    print(nome, "acc:", accuracy_score(y, p), "| F1 macro:", f1_score(y, p, average="macro"))
	Treino	Teste	Diferença
Acurácia	0,549	0,500	−0,049
F1 macro	0,466	0,411	−0,055

Como referência adicional, a acurácia média na validação cruzada temporal (TimeSeriesSplit, só no treino) foi de 0,533.

Leitura:

Diferença grande (ex.: treino 0,95 e teste 0,50) → overfitting: o modelo decorou os jogos de treino. No KNN isso é comum com k pequeno (com k=1, o treino chega perto de 100%, porque cada ponto é seu próprio vizinho).
Treino e teste baixos e parecidos → underfitting: faltam atributos informativos, ou k grande demais.
Treino e teste próximos e razoáveis → bom ajuste.
Conclusão: não há overfitting relevante. A queda do treino para o teste é de cerca de 5 p.p. (0,549 → 0,500), pequena para um KNN, e o k escolhido (35, em uma grade de 5 a 151) suaviza a decisão. Os melhores resultados da grade são quase iguais (0,528 a 0,533 para k entre 35 e 101), então a escolha exata do k pouco importa. O desempenho é baixo tanto no treino quanto no teste, o que aponta para limite de informação nos atributos (leve underfitting), e não para memorização. A escolha de k foi feita por validação cruzada temporal só no treino, sem olhar o teste.
7. Verificação de resultado bom demais

O desempenho não ficou alto (acurácia 0,500; F1 macro 0,411), mas investiguei as três causas mesmo assim:

Verificação	Como checar	Resultado
Vazamento de dados	Listar as colunas usadas em X. Atributos medidos durante/depois da partida (gols, posse, finalizações, escanteios do próprio jogo) entregam o resultado. Só podem entrar estatísticas anteriores à partida (médias das últimas N partidas).	Sem vazamento. Todos os 11 atributos são médias móveis calculadas com shift(1) (exclui o jogo atual) sobre os 5 ou 10 jogos anteriores do time, mais mando. Os valores do próprio jogo (gols, posse etc.) não entram em X.
Duplicatas antes da divisão	df.duplicated().sum() e df.duplicated(subset=["data","mandante","visitante"]).sum()	0 linhas duplicadas: nenhuma linha inteira repetida e nenhum par (fixture_id, team_id) repetido. A base tem 2.051 partidas: 1.395 aparecem em duas linhas (uma para cada time, quando ambos têm linha própria) e 656 em uma só. Isso é a visão espelhada, não duplicata, e não vaza entre treino e teste, porque a divisão é por data e as duas linhas têm a mesma data.
Divisão aleatória em dados cronológicos	Comparar train_test_split aleatório com divisão temporal (treinar nas partidas antigas, testar nas mais recentes)	Já usa divisão temporal (treino até 2024-12-04, teste de 2024-12-07 a 2026-05-17) e TimeSeriesSplit na validação. Comparação feita com o mesmo modelo (k=35), média de 20 divisões aleatórias 80/20: acurácia 0,509 (±0,014) e F1 macro 0,419, contra 0,500 e 0,411 na divisão temporal. Agrupando as duas linhas de cada partida, o resultado é o mesmo (0,508). Como a divisão aleatória não é melhor de forma relevante, não há sinal de vazamento temporal.

Pontos específicos deste projeto para olhar com atenção:

Os arquivos celtic_partidas_estatisticas_nomeadas.csv e rangers_partidas_estatisticas_nomeadas.csv são separados por time. Jogos entre Celtic e Rangers aparecem nos dois, o que explica parte das partidas com duas linhas. No notebook isso é tratado com a divisão por data (as duas linhas ficam do mesmo lado) e com drop_duplicates(["fixture_id","team_id"]) no cálculo da forma em pontos.
O mesmo jogo pode aparecer em duas linhas (visão de cada time). Como a divisão é por data (<= data_corte no treino, > data_corte no teste), as duas linhas nunca se separam entre treino e teste.
KNN usa distância: o StandardScaler está dentro do Pipeline, então é ajustado só nos dados de treino (e, na busca, só dentro de cada divisão da validação cruzada). Não há ajuste na base inteira antes da divisão.
O modelo final (modelo_final) é treinado na base inteira só para gerar previsões futuras na função prever. As métricas deste relatório vêm do modelo treinado somente no treino.
python
# Divisão temporal (compara com a aleatória)
df = df.sort_values("data")
corte = int(len(df) * 0.8)
treino, teste = df.iloc[:corte], df.iloc[corte:]

Conclusão da verificação: não foi encontrado vazamento, e o desempenho modesto (0,500 de acurácia, bem abaixo do que um vazamento produziria) é coerente com isso. Os cuidados (atributos só do passado com shift(1), divisão temporal, scaler dentro do pipeline) já estão aplicados, então não houve correção a fazer.

Próximos passos para melhorar o empate (sugestões, ainda não aplicadas): usar predict_proba e prever empate quando a diferença entre as probabilidades de vitória e derrota for pequena, ou incluir atributos que descrevam equilíbrio entre os times (ex.: abs(dif_pts_10)).

8. Slides preliminares da AP2

Entregues em arquivo separado: slides_ap2_preliminar.pptx.

Declaração de uso de I.A.

Uso de I.A. para estruturar este relatório e gerar o esqueleto dos slides, com revisão e preenchimento dos resultados pelo autor.