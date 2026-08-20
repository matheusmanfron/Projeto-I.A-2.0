# 🤖 Fut Analitics

---

## 📌 Problema

Existe no mercado, muitas ferramentas de automação usando I.A, uma delas é o famoso chatbot, muito útil para realizar atendimentos por exemplo, mas nenhum deles é direcionado ao um certo nicho e acabam sendo muito generalistas e pouco eficientes em tarefas específicas. Por isso, o projeto Fut Analitics tem o objetivo de criar um chat bot que pode prever com base em dados, resultados de uma partida de futebol e suas demais estatísticas.

---

## 🔗 Relação do projeto e uma aplicação de I.A

Acredito que uma I.A desenvolvida para ter a capacidade de prever um resultado de uma partida de futebol com base em dados e estatísticas de partidas anteriores, é o método que mais se aproxima ao realismo de uma previsão.

---

## 🧠 Tipo de problema

O projeto se encaixa mais no conceito de previsão, pois o algoritmo vai consultar dados para fazer uma previsão de um resultado esportivo e suas estatísticas.

---

## 📥 Entradas e saídas necessárias

**Entrada esperada:**

> Opa chat, qual é a previsão entre Flamengo x Palmeiras?.

**Saída da I.A:**

> Flamengo: 58%
Empate: 24%
Palmeiras: 18%

Mais de 2.5 gols: 56%
Ambas marcam: 59%
Escanteios esperados: 10,2
Gols esperados: 2,4
---

## 🏢 Duas soluções semelhantes no mercado

### DeepBetting

Focada em futebol (principais ligas da Europa) e esportes americanos (NBA, NFL, NHL e MLB). Analisa modelos estatísticos sem viés humano para sugerir probabilidades de vitória e totais de pontos/gols.

### Rithmm

Uma das plataformas mais conhecidas do segmento. Ela permite que o usuário crie modelos preditivos personalizados baseados nos dados que considera mais importantes (como eficiência defensiva ou saldo de pontos), oferecendo previsões para NBA, futebol europeu, basquete universitário e NFL.

---

## ⚠️ Limitações iniciais

* Limitações de dados por conta da pouca base da dados inicias.
* No esporte como o futebol, nenhuma previsão é 100% assertiva, pois este é muito imprevisível e qualquer coisa pode acontecer.
* Necessário dados históricos de qualidade e dados em tempo real.

---

## 💡 Por que o uso da I.A?

Pois o uso de uma I.A treinada com diversos dados, pode ter uma porcentagem de assertividade maior, tornando as previsões mais confiáveis.

---

## 📚 Fontes de dados

* StatsBomb Open Data: A StatsBomb disponibiliza gratuitamente em seu repositório no GitHub dados históricos ricos e detalhados de eventos (passes, chutes, pressão) de campeonatos específicos.
  
* TheSportsDB: Base de dados aberta mantida pela comunidade. Oferece uma API JSON gratuita ideal para obter metadados de ligas, históricos de partidas, detalhes de times e elencos em futebol, basquete, e outros esportes.

---

## 🤖 Abordagens consideradas

| Abordagem | Como funcionaria | Vantagens | Desvantagens | Viabilidade |
| --- | --- | --- | --- | --- |
| **Machine Learning (Classificação/Previsão)** | Modelo treinado com dados históricos de partidas, como vitórias, empates, derrotas, gols, finalizações, escanteios e desempenho recente. A partir dos dados das equipes, o modelo calcularia as probabilidades de vitória, empate e derrota, além de outras estatísticas. | Aprende padrões dos dados; trabalha com diversas variáveis; pode atingir boa precisão com uma base histórica adequada; permite gerar diferentes previsões estatísticas. | Necessita de uma base de dados grande e confiável; resultados podem ser afetados por dados incompletos; risco de overfitting; o futebol possui fatores imprevisíveis. | **Alta** — é a abordagem mais alinhada ao projeto e pode ser implementada gradualmente com Python e bibliotecas de Machine Learning. |
| **Lógica Fuzzy** | Utilizaria variáveis como força do ataque, força da defesa, fase atual e desempenho como mandante, classificadas em níveis como “baixo”, “médio” e “alto”. Regras fuzzy combinariam essas informações para estimar a força de cada equipe e auxiliar na previsão da partida. | Lida bem com informações imprecisas; regras são interpretáveis; permite representar conceitos como “time em boa fase”; pode complementar o modelo preditivo. | A definição das regras pode ser subjetiva; pode apresentar menor capacidade preditiva que Machine Learning quando há muitos dados; exige ajustes para evitar resultados inconsistentes. | **Média/Alta** — é viável como complemento ao Machine Learning, principalmente para incorporar fatores subjetivos do desempenho das equipes. |

---
  
---

## 📋 Backlog inicial

| # | Tarefa                          |
| - | ------------------------------- |
| 1 | Escolher o tipo de modelo       |
| 2 | Baixar a base da dados          |
| 3 | Definir dados de teste e treino |
| 4 | Aplicar                         |
| 5 | Entrega Final                   |

## 👾​ Uso de I.A

O uso da I.A foi feito para pesquisar empresas que já possuem uma ferramenta semelhante á que vou desenvolver, listar limitações no meu projeto e para reformatar o README.MD
