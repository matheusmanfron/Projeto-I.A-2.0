Autoanálise do projeto FutAnalytics

Após a apresentação da AP1, apresento os pontos positivos e negativos do meu projeto:

Pontos positivos:
	Escolha da fonte de dados: Como fonte de dados para obter o dataset, utilizei o site SportMonks, que disponibiliza uma API gratuita para consultar dados de equipes de diversas ligas esportivas. Embora a versão gratuita (que utilizo no momento) limite a busca a apenas duas ligas de futebol — no meu caso, escolhi a liga escocesa —, a plataforma oferece uma base de dados adequada para o início do desenvolvimento. É relativamente simples de usar e conta com atualizações constantes, garantindo dados condizentes com a temporada atual dos times.
	
	Ferramentas Python: Outro ponto de destaque são os scripts em Python desenvolvidos para me auxiliar na padronização dos dados e na análise geral do dataset, transformando os resultados em representações visuais claras. Embora tenha gerado esses códigos com o auxílio de IA, eu já possuía conhecimento prévio das bibliotecas pandas e scikit-learn devido ao estágio e a cursos de análise de dados e machine learning.

Pontos negativos:
	Organização: Conforme o projeto cresceu com a inclusão de novas etapas, não me atentei à organização do repositório. Como resultado, diversos arquivos ficaram desordenados. Antes de realizar qualquer alteração estrutural, reorganizarei as pastas e arquivos para garantir fácil entendimento nas próximas avaliações, além de incluir os arquivos de notebooks que faltam.

	Base de dados reduzida: Como utilizei apenas dados de dois times da Escócia — justamente os maiores do país —, surgiu um problema de viés e uma quantidade insuficiente de dados para o treinamento do modelo de IA. Como solução, coletarei dados de todos os 12 times da liga e expandirei o histórico de 10 para 100 partidas por equipe, elevando o volume de 20 para 1.200 registros (uma base ainda enxuta, porém funcional).

Backlog do projeto:
	[/] Organização do repositório
	[ ] Criação dos notebooks no Google Colab
	[ ] Aumento da base de dados
	[ ] Padronização dos dados
	[ ] Treinamento do modelo de IA
	[ ] Testes do modelo