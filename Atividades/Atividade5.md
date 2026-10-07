1 - Diagnóstico dos problemas de qualidade
    Os dados foram retirados do site SportMonks e a base é formada por 2 CSVs, celtic_partidas e rangers_partidas.

    #Dimensões totais = 20 linhas;
                        19 colunas;
                        380 células;
                        18 partidas concluídas;
                        2 partidas ainda não concluídas no momento da coleta.

    #Dados faltantes = 
                        | Coluna                    | Valores ausentes | Proporção |
                        | Cartões vermelhos         |               17 |       85% |

    #Dados duplicados = Sem dados duplicados

    #Inconsitências = Não foi encontrado grandes incocistências na base de dados, mas existem pontos que exigem atenção.
                      A coluna resultado não está padronizada para o problema de classificação e 
                      os valores de season_id encontrados são 25598 e 28275, mas seria melhor se tivesse uma ordem cronologica para as temporadas.

    #Desbalanceamento de dados = 
                        | Classe    | Quantidade | Proporção |
                        | --------- | ---------: | --------: |
                        | Vitória   |         12 |    66,67% |
                        | Derrota   |          5 |    27,78% |
                        | Empate    |          1 |     5,56% |
                        | **Total** |     **18** |  **100%** |

2 - Tabela diagnostico = 
        | Problema encontrado                        | Onde aparece                                  | Gravidade | Ação de tratamento proposta                                                                       | Quando será tratado             |
        | ------------------------------------------ | --------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------- | ------------------------------- |
        | Partidas não concluídas                    | Registros com `state_id = 10`                 | Alta      | Atualizar os dados após as partidas ou remover esses registros do treinamento                     | Resolvido                   |
        | Resultados ausentes                        | Coluna `resultado`, 2 registros               | Alta      | Não utilizar registros sem resultado como exemplos de treinamento                                 | Resolvido                    |
        | Estatísticas ausentes                      | Duas partidas de 22/08/2026                   | Alta      | Buscar novamente os dados ou excluir temporariamente os registros                                 | Resolvido                      |
        | Assistências ausentes                      | `Assistências`, 4 registros                   | Média     | Verificar a API e, se não for possível recuperar, avaliar a remoção da variável                   | Resolvido parcialmente                     |
        | Resultado textual não padronizado          | Coluna `resultado`                            | Alta      | Converter para Vitória, Empate e Derrota pela perspectiva do time da linha                        | Resolvido de outra forma                      |
        | Repetição de `fixture_id`                  | Partida `19700214`                            | Baixa     | Utilizar `fixture_id + team_id` como chave composta                                               | Na consolidação                 |
        | Data possivelmente armazenada como texto   | Coluna `data`                                 | Média     | Converter para o tipo `datetime`                                                                  | Encontro 8                      |
        | Duas temporadas na mesma base              | Coluna `season_id`                            | Média     | Manter a informação e realizar divisão cronológica dos dados                                      | Antes do treinamento            |
        | Classes desbalanceadas                     | Variável de saída                             | Alta      | Aumentar a base e usar métricas adequadas por classe                                              | Antes e durante o treinamento   |
        | Identificadores sem valor esportivo direto | Colunas de IDs                                | Média     | Manter para rastreamento, mas retirar das entradas do modelo                                      | Preparação do treinamento       |
        | Risco de vazamento da resposta             | Estatísticas da própria partida               | Alta      | Criar médias móveis usando somente partidas anteriores                                            | Construção das variáveis        |

3 - Ações de tratamentos propostas
    As partidas ainda não concluídas não serão utilizadas no treinamento enquanto estiverem sem resultado. Primeiro será feita uma nova consulta à API. Caso as informações continuem indisponíveis, esses registros serão removidos temporariamente da base de treinamento, mas poderão ser preservados em um arquivo separado para atualização futura.
    A coluna resultado será transformada em uma variável com três classes:

    0: derrota;
    1: empate;
    2: vitória.

    Essa transformação será feita considerando o time informado na coluna time. Por exemplo, se a linha representa o Rangers e o resultado informa que o Celtic venceu, a classe correta para aquela linha será Derrota.

    Na coluna Cartões vermelhos, será necessário verificar se a Sportmonks omite essa estatística quando o valor é zero. Se isso for confirmado, os campos ausentes poderão ser preenchidos com zero. Caso contrário, os valores deverão continuar como ausentes ou a variável poderá ser retirada do primeiro modelo.

    A coluna data será convertida para data e hora. Isso permitirá ordenar as partidas cronologicamente e garantir que as médias utilizadas para prever uma partida sejam calculadas somente com dados anteriores a ela.

4 - Discussão de possíveis viés:
    A base representa somente partidas da liga escocesa masculina e, mais especificamente, registros coletados pela perspectiva de Celtic e Rangers. Assim, ficaram de fora outras ligas, o futebol feminino, divisões inferiores e equipes com características esportivas e financeiras diferentes.

    Também existe um viés de seleção das equipes. Celtic e Rangers são dois dos clubes mais fortes e conhecidos da Escócia. Na base atual, o Celtic venceu todas as nove partidas concluídas registradas. Por isso, o modelo pode aprender um padrão exageradamente favorável a equipes dominantes e não conseguir generalizar para confrontos entre clubes de nível semelhante.
