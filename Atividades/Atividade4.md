1. Base de dados consolidada

A base utilizada neste projeto foi construída a partir de dados obtidos pela Sportmonks Football API, utilizando partidas da Scottish Premiership.

Foram utilizados inicialmente dois conjuntos de dados:

Celtic — team_id = 53
Rangers — team_id = 62

Os dados foram obtidos através do endpoint de partidas da Sportmonks e 
posteriormente filtrados para manter as informações da partida e as estatísticas das equipes.

A Sportmonks disponibiliza os dados em formato JSON e permite incluir estatísticas de 
uma partida através do parâmetro include=statistics. A API também permite retornar 
informações relacionadas em uma mesma requisição.

Estrutura atual da base

A base consolidada possui informações relacionadas a:

identificação da partida;
data;
equipes;
adversário;
mando de campo;
liga;
temporada;
resultado;
estatísticas de desempenho.

As estatísticas disponíveis nos dados coletados incluem:

Escanteios;
Posse de bola;
Gols;
Assistências;
Cartões vermelhos;
Cartões amarelos;
Dribles bem-sucedidos.

A Sportmonks informa que suas estatísticas de partidas podem incluir métricas como posse, chutes, passes, escanteios e outras estatísticas por equipe.

2. Origem da base de dados
Fonte

Sportmonks Football API

A Sportmonks fornece dados históricos e atuais de partidas de futebol por meio de uma 
API REST que retorna os dados em formato JSON. A plataforma disponibiliza informações de 
partidas, equipes, estatísticas, escalações, eventos e outras informações relacionadas ao futebol.

Site oficial:

Sportmonks Football API = https://www.sportmonks.com/

Plano utilizado:

Foi utilizada a modalidade gratuita da Sportmonks. Atualmente, o plano gratuito disponibiliza, 
entre outras competições, a Scottish Premiership, incluindo suas estatísticas.

Data de acesso: 27/08/2026.

Forma de obtenção

Os dados foram obtidos através de requisições HTTP à API da Sportmonks utilizando um token de autenticação.

Para consultar partidas e estatísticas, foram utilizados endpoints da estrutura:

https://api.sportmonks.com/v3/football/fixtures/

A Sportmonks permite adicionar estatísticas de uma partida utilizando o parâmetro:

?include=statistics

Uma única requisição pode retornar a partida juntamente com suas estatísticas, reduzindo a necessidade 
de realizar várias consultas separadas.

Condições de uso

Os dados são utilizados neste projeto para fins de estudo, análise e desenvolvimento de um 
protótipo de Machine Learning. A utilização deve respeitar os termos de serviço da Sportmonks 
e as condições aplicáveis ao plano utilizado.

As consultas realizadas para obter dados dos dois times foram essas:
Celtic = https://api.sportmonks.com/v3/football/fixtures/between/2025-08-01/2026-08-27/53?api_token=SECRETO&order=desc&per_page=10&include=participants;statistics;scores
Rangers = https://api.sportmonks.com/v3/football/fixtures/between/2025-08-01/2026-08-27/62?api_token=SECRETO&order=desc&per_page=10&include=participants;statistics;scores

3. Dicionário de dados

O dicionário de dados descreve as principais variáveis utilizadas na base e sua finalidade dentro do projeto.

Variável	Tipo	Descrição
fixture_id	Inteiro	Identificador único da partida na Sportmonks.
data	Data/hora	Data e horário de início da partida.
partida	Categórica	Nome das duas equipes que disputaram a partida.
time	Categórica	Equipe que está sendo analisada.
team_id	Inteiro	Identificador da equipe na Sportmonks.
local_visitante	Categórica	Indica se a equipe analisada jogou em casa ou fora.
adversario	Categórica	Nome da equipe adversária.
adversario_id	Inteiro	Identificador da equipe adversária.
resultado	Categórica	Resultado textual da partida.
league_id	Inteiro	Identificador da competição.
season_id	Inteiro	Identificador da temporada.
state_id	Inteiro	Identificador do estado da partida.
Escanteios	Numérica	Quantidade de escanteios da equipe durante a partida.
Posse de bola (%)	Numérica	Percentual de posse de bola da equipe.
Gols	Numérica	Quantidade de gols marcados pela equipe.
Assistências	Numérica	Quantidade de assistências registradas para a equipe.
Cartões vermelhos	Numérica	Quantidade de cartões vermelhos recebidos pela equipe.
Cartões amarelos	Numérica	Quantidade de cartões amarelos recebidos pela equipe.
Dribles bem-sucedidos (%)	Numérica	Percentual de dribles realizados com sucesso.

A Sportmonks identifica as estatísticas de equipe por meio de type_id, participant_id, location e data.value, sendo o data.value o valor efetivamente observado para aquela estatística.

type 34  → Escanteios
type 45  → Posse de bola (%)
type 52  → Gols
type 79  → Assistências
type 83  → Cartões vermelhos
type 84  → Cartões amarelos
type 1605 → % dribles bem-sucedidos

4. Variáveis de entrada e saída

O objetivo do projeto é desenvolver um modelo capaz de prever o resultado de uma partida de futebol com base no desempenho recente das equipes.

Por isso, as variáveis de entrada não devem ser simplesmente os dados de uma única partida. A proposta é calcular características baseadas nas últimas 10 partidas de cada equipe.

Variáveis de entrada

Inicialmente, serão consideradas:

Média de gols
Média de escanteios
Média de posse de bola
Média de assistências
Média de cartões amarelos
Média de cartões vermelhos
Média de dribles bem-sucedidos

Essas informações podem ser calculadas separadamente para cada equipe.

Por exemplo:

Celtic:

média_gols = 2.1
média_escanteios = 6.8
média_posse = 61.4%
...

e:

Rangers:

média_gols = 1.7
média_escanteios = 5.9
média_posse = 57.3%
...

Posteriormente, também poderão ser criadas variáveis de diferença:

diferença_gols =
média_gols_celtic - média_gols_rangers
diferença_posse =
média_posse_celtic - média_posse_rangers

Essa abordagem permite representar a vantagem estatística de uma equipe em relação à outra.

Variável de saída

A variável que pretendemos prever será o resultado da partida.

Inicialmente, ela pode ser representada por três classes:

0 → Derrota
1 → Empate
2 → Vitória

Por exemplo:

Celtic 2 × 1 Rangers

Resultado → Vitória do Celtic

O problema, portanto, será tratado inicialmente como um problema de classificação multiclasse.

5. Análise estatística inicial

A análise estatística tem como objetivo compreender o comportamento dos dados antes do treinamento do modelo.

As principais medidas que serão utilizadas são:

média;
desvio padrão;
mínimo;
máximo;
frequência;
quantidade de valores ausentes.
Média

A média será utilizada para representar o desempenho médio de uma equipe nas partidas anteriores.

Por exemplo:

Média de gols = 2,0

significa que, considerando as partidas analisadas, a equipe marcou aproximadamente dois gols por partida, em média.

Essa informação pode representar uma indicação inicial do poder ofensivo da equipe.

Desvio padrão

O desvio padrão será utilizado para avaliar a variabilidade do desempenho.

Por exemplo:

Média de gols = 2,0
Desvio padrão = 0,5

indica que a quantidade de gols tende a variar pouco em relação à média.

Por outro lado:

Média de gols = 2,0
Desvio padrão = 1,5

indicaria um desempenho muito mais irregular.

Essa informação é importante porque duas equipes podem possuir a mesma média, mas apresentar comportamentos bastante diferentes.

Frequência dos resultados

Também devemos observar quantas partidas terminaram em:

Vitória
Empate
Derrota

Isso permite identificar se existe algum desequilíbrio na variável de saída.

Por exemplo, se tivermos:

Vitória: 15
Empate: 3
Derrota: 2

a classe "Vitória" estaria muito mais representada que as demais.

Nesse caso, um modelo poderia aprender a favorecer excessivamente essa classe.

Interpretação inicial

A análise estatística da base deve ser utilizada não apenas para apresentar números, mas para identificar padrões.

As médias das estatísticas ofensivas, como gols, escanteios e posse de bola, podem indicar diferenças de desempenho entre as equipes. Já cartões e dribles podem fornecer informações complementares relacionadas à disciplina e ao comportamento ofensivo.

Entretanto, a base atual ainda é pequena, portanto as médias obtidas devem ser consideradas apenas como uma análise exploratória inicial e não como evidência estatística definitiva.

6. Visualização

Uma visualização inicial recomendada é um gráfico comparando as médias das principais estatísticas do Celtic e do Rangers.

Por exemplo:

              Celtic        Rangers

Gols             ████████      ██████
Escanteios       █████████     ███████
Posse             ██████████    █████████
Assistências      ██████        █████

O gráfico permite observar visualmente diferenças entre os desempenhos médios das equipes.

Interpretação

Uma equipe que apresenta maior média de gols pode possuir maior capacidade ofensiva.

Uma maior média de posse pode indicar maior controle das partidas, enquanto uma maior média de escanteios pode representar maior volume de pressão ofensiva.

Entretanto, nenhuma dessas variáveis isoladamente é suficiente para determinar o vencedor. O objetivo do Machine Learning será justamente encontrar relações entre várias características simultaneamente.

A Sportmonks disponibiliza estatísticas de equipe por partida, permitindo análises desse tipo.

7. Primeiras observações sobre a base

Durante a preparação dos dados, foram identificados alguns pontos que precisam ser considerados antes do treinamento do modelo.

7.1 Poucas linhas

A principal limitação atual é o tamanho reduzido da base.

Atualmente estamos trabalhando principalmente com:

Celtic
Rangers

e suas partidas coletadas.

Isso é suficiente para desenvolver e testar o pipeline de tratamento dos dados, mas é insuficiente para treinar um modelo de Machine Learning robusto.

Solução futura

Expandir a base para:

Celtic
Rangers
Hearts
Hibernian
Aberdeen
...

e, se possível, utilizar várias temporadas.

7.2 Valores ausentes

Algumas partidas podem apresentar:

"statistics": []

Isso significa que não existem estatísticas disponíveis naquela resposta para a partida.

Portanto, antes do treinamento será necessário verificar:

Quantidade de valores ausentes
Percentual de valores ausentes

e decidir entre:

remover determinadas partidas;
preencher valores;
buscar novamente os dados;
ou utilizar somente partidas com estatísticas completas.

Não devemos simplesmente substituir todos os valores ausentes por zero, pois ausência de informação não significa necessariamente que a equipe teve valor zero naquela estatística.

7.3 Temporadas diferentes

Como a consulta foi realizada por intervalo de datas, a base pode conter partidas de mais de uma temporada.

Por isso existe a variável:

season_id

Ela será importante para identificar a temporada de cada partida.

Podemos posteriormente decidir se o modelo deverá:

utilizar várias temporadas;
utilizar somente a temporada atual;
ou utilizar temporadas anteriores como histórico.
7.4 Colunas potencialmente irrelevantes

Algumas variáveis provavelmente não deverão entrar diretamente no modelo.

Por exemplo:

fixture_id
team_id
adversario_id
league_id

Esses valores são principalmente identificadores.

O fixture_id, por exemplo, identifica uma partida, mas não possui uma relação direta com o desempenho esportivo.

Portanto, essas informações são importantes para organizar e rastrear os dados, mas não necessariamente como variáveis de entrada do modelo.

7.5 Pouca diversidade de equipes

Utilizar somente Celtic e Rangers cria outro problema: o modelo pode acabar aprendendo características muito específicas dessas duas equipes.

Para um modelo capaz de prever partidas de maneira mais geral, será necessário aumentar a diversidade da base.
