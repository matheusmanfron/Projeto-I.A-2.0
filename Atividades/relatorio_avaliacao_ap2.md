# 🤖 Fut Analitics — Avaliação do Modelo (AP2)

**Modelo:** KNN (K-Nearest Neighbors) · **Notebook:** `ModeloKNN.ipynb` · **Dados:** `Partidas_Tratadas.csv` (Scottish Premiership, via SportMonks)
**Problema:** classificação do resultado da partida em **Vitória do mandante / Empate / Vitória do visitante**.

> ⚠️ **Como usar este documento.** Não consegui abrir o notebook nem os resultados da Atividade 9 pelo GitHub (a página pública mostra só o README). Por isso **nenhum número aqui foi inventado**: onde aparece `[PREENCHER]`, rode a célula de código indicada no notebook e cole o valor. Se as classes do seu modelo forem outras (ex.: só vitória/não vitória), ajuste os nomes nas seções 4 e 5.

---

## 1. Métricas (classificação)

Como é classificação, as métricas são acurácia, precisão, recall e F1, geradas pelo `classification_report`.

```python
from sklearn.metrics import classification_report, accuracy_score

y_pred = modelo.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, digits=3))
```

| Classe | Precisão | Recall | F1-score | Suporte |
|---|---|---|---|---|
| Vitória mandante | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Empate | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Vitória visitante | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| **Acurácia** | | | [PREENCHER] | [PREENCHER] |
| **Macro avg** | [PREENCHER] | [PREENCHER] | [PREENCHER] | |

**Leitura:** [PREENCHER — ex.: qual classe o modelo acerta melhor e qual ele quase nunca acerta. No futebol, o empate costuma ter o menor recall.]

---

## 2. Matriz de confusão

```python
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, cmap="Blues", xticks_rotation=20
)
plt.title("Matriz de confusão — KNN (teste)")
plt.show()
```

*(Insira aqui a imagem gerada, ex.: `![matriz](matriz_confusao.png)` após `plt.savefig("matriz_confusao.png", dpi=150)`.)*

**Como interpretar** (a diagonal principal são os acertos; fora dela, os erros):

- Linhas = resultado real; colunas = previsão do modelo.
- Maior erro identificado: [PREENCHER — ex.: "Empates reais previstos como vitória do mandante: N casos"].
- Confusão típica do futebol: o modelo tende a "empurrar" jogos equilibrados para a vitória do mandante, porque ela costuma ser a classe mais frequente.
- Conclusão: [PREENCHER — o que o padrão de erros diz sobre os dados/atributos usados].

---

## 3. Comparação com o baseline (Atividade 9)

```python
from sklearn.dummy import DummyClassifier

baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
yb = baseline.predict(X_test)
# Use o MESMO baseline e a MESMA divisão da Atividade 9.
```

| Métrica (teste) | Baseline (Atividade 9) | KNN (meu modelo) | Diferença |
|---|---|---|---|
| Acurácia | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| F1 macro | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Recall do empate | [PREENCHER] | [PREENCHER] | [PREENCHER] |

**Veredito explícito:** o KNN **[SUPERA / NÃO SUPERA]** o baseline em [PREENCHER métrica], por [PREENCHER] pontos.

> Cuidado: se o baseline é "sempre prever a classe mais frequente", ele pode ter acurácia razoável e F1 macro baixíssimo. Compare as duas métricas, e não só a acurácia.

---

## 4. Significado dos erros no domínio

Em um problema de 3 classes, falso positivo e falso negativo existem **para cada classe**. Na linguagem do futebol, usando "vitória do mandante" como exemplo:

- **Falso positivo (alarme falso):** o Fut Analitics diz "o mandante vai ganhar", mas o jogo termina em empate ou vitória do visitante. Quem confiou na previsão se prepara para um cenário que não aconteceu.
- **Falso negativo (deixar passar):** o mandante ganha, mas o modelo previu empate ou vitória do visitante. O usuário descarta uma vitória que ia acontecer.

Para as outras classes:

| Classe | Falso positivo significa | Falso negativo significa |
|---|---|---|
| Empate | Previu igualdade, e um time venceu | Houve empate e o modelo não viu (erro mais comum) |
| Vitória visitante | Previu surpresa fora de casa, e ela não veio | O visitante venceu e o modelo não percebeu a zebra |

---

## 5. Métrica principal e justificativa

**Métrica principal: F1-score macro** (média do F1 das três classes).

**Por quê:**

1. **A acurácia engana.** Com classes desbalanceadas (vitórias do mandante dominam), um modelo que ignora o empate ainda parece bom. O F1 macro dá o mesmo peso às três classes.
2. **Custo do erro.** O Fut Analitics entrega probabilidades que o usuário usa para decidir. Aqui o **alarme falso é mais caro**: uma previsão confiante e errada gera falsa segurança. Já deixar passar um resultado apenas torna a previsão menos útil, sem induzir uma decisão errada.
3. Por isso acompanho a **precisão** das classes de vitória como métrica secundária, e o F1 macro garante que o modelo não "desista" do empate.

> Se o seu professor/grupo entende que o custo maior é deixar passar (ex.: não detectar uma zebra), troque a justificativa e a métrica principal para o **recall** da classe correspondente.

---

## 6. Teste de overfitting

```python
from sklearn.metrics import accuracy_score, f1_score

for nome, X, y in [("treino", X_train, y_train), ("teste", X_test, y_test)]:
    p = modelo.predict(X)
    print(nome, "acc:", accuracy_score(y, p), "| F1 macro:", f1_score(y, p, average="macro"))
```

| | Treino | Teste | Diferença |
|---|---|---|---|
| Acurácia | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| F1 macro | [PREENCHER] | [PREENCHER] | [PREENCHER] |

**Leitura:**

- Diferença grande (ex.: treino 0,95 e teste 0,50) → **overfitting**: o modelo decorou os jogos de treino. No KNN isso é comum com `k` pequeno (com `k=1`, o treino chega perto de 100%, porque cada ponto é seu próprio vizinho).
- Treino e teste baixos e parecidos → **underfitting**: faltam atributos informativos, ou `k` grande demais.
- Treino e teste próximos e razoáveis → bom ajuste.
- Conclusão: [PREENCHER]. Teste valores de `k` (ex.: 3, 5, 9, 15) e escolha com validação cruzada, nunca olhando o teste.

---

## 7. Verificação de resultado bom demais

Se o desempenho ficou alto, antes de comemorar investiguei três causas:

| Verificação | Como checar | Resultado |
|---|---|---|
| **Vazamento de dados** | Listar as colunas usadas em `X`. Atributos medidos **durante/depois** da partida (gols, posse, finalizações, escanteios do próprio jogo) entregam o resultado. Só podem entrar estatísticas **anteriores** à partida (médias das últimas N partidas). | [PREENCHER] |
| **Duplicatas antes da divisão** | `df.duplicated().sum()` e `df.duplicated(subset=["data","mandante","visitante"]).sum()` | [PREENCHER] |
| **Divisão aleatória em dados cronológicos** | Comparar `train_test_split` aleatório com divisão temporal (treinar nas partidas antigas, testar nas mais recentes) | [PREENCHER] |

Pontos específicos deste projeto para olhar com atenção:

- Os arquivos `celtic_partidas_estatisticas_nomeadas.csv` e `rangers_partidas_estatisticas_nomeadas.csv` são separados por time. **Jogos entre Celtic e Rangers aparecem nos dois**, então podem virar duplicatas. Remova antes de dividir.
- O mesmo jogo pode aparecer em duas linhas (visão do mandante e do visitante). Se uma linha cair no treino e a outra no teste, o modelo "já viu" a resposta.
- **KNN usa distância**: o `StandardScaler` deve ser ajustado só no treino (`fit` no treino, `transform` no teste). Ajustar na base inteira também é vazamento.

```python
# Divisão temporal (compara com a aleatória)
df = df.sort_values("data")
corte = int(len(df) * 0.8)
treino, teste = df.iloc[:corte], df.iloc[corte:]
```

**Conclusão da verificação:** [PREENCHER — o que foi encontrado e corrigido, e qual o desempenho **depois** da correção].

---

## 8. Slides preliminares da AP2

Entregues em arquivo separado: `slides_ap2_preliminar.pptx`.

---

## Declaração de uso de I.A.

Uso de I.A. para estruturar este relatório e gerar o esqueleto dos slides, com revisão e preenchimento dos resultados pelo autor.
