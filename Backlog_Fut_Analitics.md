# Backlog do projeto — Fut Analitics

**Projeto:** Fut Analitics — previsão de resultados de partidas de futebol com aprendizado de máquina  
**Repositório:** https://github.com/matheusmanfron/Projeto-I.A-2.0  
**Atualização:** 04/11/2026  
**Domínio:** Campeonato Escocês de futebol  
**Legenda:** `[x]` concluído · `[~]` parcialmente concluído / requer revisão · `[ ]` pendente

## 1. Objetivo

Desenvolver um sistema capaz de utilizar estatísticas históricas de partidas para prever, do ponto de vista de uma equipe, **derrota (0), empate (1) ou vitória (2)**. A visão inicial do projeto inclui apresentar probabilidades e, futuramente, estimativas de gols e outras estatísticas em uma interface de consulta. Até o momento, há modelos e análises experimentais; a interface completa e as previsões adicionais ainda não foram demonstradas como concluídas.

## 2. Backlog consolidado

| ID | Etapa / atividade | Status | Evidência e resultado | Próximo passo, se necessário |
|---|---|---|---|---|
| 01 | Definir problema, domínio e público-alvo | [x] | Projeto Fut Analitics descrito no `README.md`; previsão de partidas de futebol | Manter escopo documentado |
| 02 | Escolher fonte de dados | [x] | API SportMonks definida como fonte principal | Documentar limites e atualização dos dados |
| 03 | Implementar consulta e exportação dos dados | [x] | Scripts de consulta/exportação em `ScriptsPython/`, incluindo `exportar_partidas_sportmonks_csv.py` | Validar consultas em novas temporadas |
| 04 | Expandir cobertura da base | [x] | Expansão inicial de 2 times/10 partidas para 12 equipes, com registros históricos; descrita no README | Verificar cobertura e distribuição por equipe/temporada |
| 05 | Consolidar arquivos e estruturar CSV | [x] | Pastas `Dados/` e scripts de compactação/exportação | Manter rastreabilidade da base utilizada em cada experimento |
| 06 | Diagnosticar qualidade dos dados | [x] | Atividades de diagnóstico de ausentes, tipos, duplicidades e inconsistências | Repetir diagnóstico quando a base mudar |
| 07 | Tratar e padronizar os dados | [x] | Notebook `Tratamento_Base.ipynb` e base tratada utilizada nos experimentos | Automatizar verificações e registrar regras de tratamento |
| 08 | Definir variáveis de entrada e saída | [x] | Saída multiclasse 0/1/2; atributos históricos definidos nos notebooks | Revisar relevância das features |
| 09 | Evitar vazamento de informação | [x] | Médias históricas com `shift(1)` antes das janelas móveis, registradas na análise técnica | Criar testes automatizados de ausência de vazamento |
| 10 | Definir divisão temporal treino/teste | [x] | Separação cronológica aplicada; no experimento mais recente, 2.686 registros de treino e 670 de teste | Garantir que registros da mesma partida/data não atravessem os conjuntos |
| 11 | Criar modelo inicial KNN | [x] | `ModeloKNN.ipynb` e `ModeloKNN_Novo.ipynb` | Preservar versão de referência reproduzível |
| 12 | Padronizar atributos e ajustar hiperparâmetros | [x] | `StandardScaler`, busca de parâmetros e validação temporal documentadas | Registrar configuração final por experimento |
| 13 | Comparar com baselines | [x] | Baseline da classe majoritária e regra de mando comparados ao KNN na AP2 | Manter baselines nas próximas avaliações |
| 14 | Avaliar classificação e erros | [x] | Acurácia, precisão, recall, F1 macro e matriz de confusão na AP2 | Acompanhar resultados por classe e por temporada |
| 15 | Investigar especificamente os empates | [x] | Atividade 12, Caminho B: análise exploratória da taxa de erro por classe | Usar achados para novos experimentos |
| 16 | Produzir análise técnica e plano de melhoria | [x] | `Atividade11_AnaliseTecnica.md` | Priorizar melhorias antes da entrega final |
| 17 | Experimentar rede neural MLP | [x] | `Atividade13.md` e notebook `Atividade_Redes_Neurais_KNN_vs_MLP_Executado.ipynb` | Ajustar rede apenas se houver ganho demonstrável |
| 18 | Comparar KNN, MLP e baseline em condições iguais | [x] | Teste comum de 670 registros; KNN 50,0%, MLP 47,0%, baseline 40,3% de acurácia | Repetir após mudanças no pipeline |
| 19 | Decidir modelo principal provisório | [x] | Atividade 13 mantém KNN como escolha atual | Reavaliar com novas métricas e experimentos |
| 20 | Analisar aplicação semelhante no mercado | [x] | `Atividade14.md`: estudo do Forebet e relação com o Fut Analitics | Incorporar boas práticas de apresentação probabilística |
| 21 | Resolver baixo reconhecimento de empates | [ ] | KNN identifica poucos empates; recall aproximado de 0,06 na avaliação AP2 | Testar balanceamento, pesos, novas features e outros classificadores |
| 22 | Revisar generalização e overfitting | [~] | MLP: 65% no treino e 47% no teste; diferença de 18 p.p. | Testar regularização, arquitetura e validação temporal |
| 23 | Investigar aviso de convergência da MLP | [ ] | `ConvergenceWarning` após 500 épocas registrado na Atividade 13 | Testar taxa de aprendizado, tolerância, regularização e parada antecipada |
| 24 | Auditar dependência entre observações | [ ] | Relatório AP2 aponta partidas representadas do ponto de vista de ambas as equipes | Agrupar por partida e evitar contaminação entre treino, validação e teste |
| 25 | Avaliar qualidade das probabilidades | [ ] | Probabilidades fazem parte do objetivo do produto, mas não há validação de calibração concluída | Medir calibração, Brier score e log loss quando aplicáveis |
| 26 | Testar novos atributos e algoritmos | [ ] | Necessidade indicada pelas análises de erros | Comparar, por exemplo, regressão logística, árvores e Random Forest sem vazamento |
| 27 | Implementar fluxo de previsão de partida futura | [~] | Treinamento e previsão em notebooks existem; fluxo final de consulta não está comprovado | Receber duas equipes, construir features disponíveis antes do jogo e retornar previsão |
| 28 | Criar interface de usuário / chatbot | [ ] | Ideia descrita no README; implementação final não evidenciada | Definir interface simples para seleção da partida e apresentação da previsão |
| 29 | Apresentar probabilidades e limitações | [ ] | Saída desejada no README e análise do Forebet | Exibir as três probabilidades e alertar sobre incerteza |
| 30 | Estimar gols, escanteios e mercados adicionais | [ ] | Objetivo futuro apresentado no README | Tratar como modelos separados, com métricas próprias |
| 31 | Documentar execução e reproduzibilidade | [~] | Notebooks, relatórios e scripts estão versionados | Criar instruções de instalação, dependências, execução e origem dos dados |
| 32 | Consolidar relatório e apresentação final | [~] | Slides e relatórios AP2 existentes | Atualizar conclusões, limitações, resultados e demonstração para entrega final |

## 3. Resultados técnicos registrados

### Experimento comparativo mais recente (Atividade 13 / AP2)

| Modelo | Acurácia de teste | F1 macro de teste | Observação |
|---|---:|---:|---|
| Baseline — classe majoritária | 40,3% | 0,191 | Referência simples |
| KNN | **50,0%** | 0,411 | Modelo principal provisório |
| MLPClassifier | 47,0% | **0,421** | F1 macro ligeiramente superior, mas acurácia inferior e sinais de overfitting |

- **Divisão:** 2.686 registros de treinamento e 670 de teste, em ordem cronológica.
- **Atributos:** 11 características históricas, incluindo mando, pontos recentes, gols, escanteios, posse, cartões e desempenho do adversário.
- **KNN:** `n_neighbors=35`, `p=2`, `weights='uniform'`, com `StandardScaler`.
- **MLP:** camadas ocultas `(32, 16)`, ativação ReLU, otimizador Adam, `max_iter=500`, `random_state=42`, com `StandardScaler`.
- **Limitação principal:** reconhecimento insuficiente de empates; na avaliação AP2, 9 dos 157 empates reais foram corretamente classificados pelo KNN.
- **Nota de rastreabilidade:** a `Atividade11_AnaliseTecnica.md` registra um experimento anterior com 3.274 observações e métricas diferentes. Não misturar seus números com os do relatório AP2, que utiliza 3.356 observações após preparação.

## 4. Próximas prioridades sugeridas

| Prioridade | Item | Critério de conclusão |
|---|---|---|
| Alta | Corrigir validação por partida/data | Nenhuma informação da mesma partida ou do futuro contamina treino e teste |
| Alta | Melhorar a identificação de empates | Aumento comprovado do recall/F1 de empate sem piora desproporcional das demais classes |
| Alta | Reproduzir experimento final | Um notebook ou script executa preparação, treino, baselines e avaliação com resultados rastreáveis |
| Média | Avaliar probabilidades | Probabilidades verificadas e acompanhadas de medidas de calibração |
| Média | Comparar novos modelos | Comparação justa, temporal e com métricas por classe |
| Média | Criar consulta de partidas futuras | Seleção de equipes gera uma previsão usando apenas dados anteriores ao jogo |
| Baixa / expansão | Criar interface e previsões adicionais | Interface utilizável e modelos específicos para gols/escanteios, se houver tempo |

## 5. Critérios para considerar o projeto finalizado

- [ ] Pipeline de dados reproduzível e sem vazamento identificado.
- [ ] Modelo final escolhido por comparação justa com baseline e alternativas.
- [ ] Métricas gerais e por classe documentadas, especialmente para empates.
- [ ] Limitações, incerteza e possibilidade de erro apresentadas claramente.
- [ ] Demonstração funcional de previsão para uma partida ainda não ocorrida, se isso estiver no escopo da entrega.
- [ ] README, relatório final e apresentação atualizados.

## 6. Referências internas

- [README do Fut Analitics](https://github.com/matheusmanfron/Projeto-I.A-2.0/blob/main/README.md)
- [Atividade 7 — Pipeline](https://github.com/matheusmanfron/Projeto-I.A-2.0/blob/main/Atividades/Atividade7.md)
- [Atividade 11 — Análise técnica](https://github.com/matheusmanfron/Projeto-I.A-2.0/blob/main/Atividades/Atividade11_AnaliseTecnica.md)
- [Atividade 12 — Análise de erros](https://github.com/matheusmanfron/Projeto-I.A-2.0/blob/main/Atividades/Atividade12.md)
- [Atividade 13 — KNN vs. MLP](https://github.com/matheusmanfron/Projeto-I.A-2.0/blob/main/Atividades/Atividade13.md)
- [Atividade 14 — Forebet](https://github.com/matheusmanfron/Projeto-I.A-2.0/blob/main/Atividades/Atividade14.md)
- [Relatório de avaliação AP2](https://github.com/matheusmanfron/Projeto-I.A-2.0/blob/main/Atividades/relatorio_avaliacao_ap2.md)

> **Observação:** os status refletem o que está documentado no repositório em 04/11/2026. Um item marcado como pendente pode ter sido desenvolvido localmente sem ainda estar registrado no GitHub.
