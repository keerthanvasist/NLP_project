# coding=UTF-8
from glob import glob
import os, nltk.test
import sys
import nltk
from collections import Counter
from summarizer import summarize

reload(sys)
sys.setdefaultencoding('utf8')
# nltk.download()
folder_year = ['/PT2010-2011','/PT2012-2013']
folder_type = "/docs"
directory_main = "PriberamCompressiveSummarizationCorpus"
def makelist(dir):
	articles_list = []
	word_list = []
	# for fold in (dir + s for s in arrayforfolds):
	for fold in (dir + f + "/docs" for f in folder_year):
		# print fold
		# fold = fold + "*.sents"
		paths = glob(fold+"/*/")
		for folder in paths:
			folder = folder + "*.sents"
			files = glob(folder)
			# print files
			for file in files:
				# print file

				fp = open(file,'r')
				article = fp.read()
				# print article
				articles_list.append(article)
				# word_list.extend(article)
	
	return articles_list


articles_corpus = makelist(directory_main)
# print articles_corpus[1]


#delete export.py,init, keywords,TextrankRuntimeError, porter


content = """
   
Um dia após o duplo atentado na Noruega, os contornos da tragédia mudaram de forma dramática.
A polícia afirma agora que não foi obra de radicais islâmicos mas sim de um atirador solitário com ligações à extrema-direita de raiz nazi.
Anders Behring Breivik, norueguês de 32 anos, foi detido e confessou ter sido ele a colocar as bombas que mataram sete pessoas no centro de Oslo, horas antes de matar a tiro pelo menos 85 outras na ilha de Utoya.
As autoridades procuravam ontem possíveis cúmplices do atirador e usaram minissubmarinos para encontrar, nas águas do lago que cerca a ilha, seis pessoas dadas como desaparecidas.
Os relatos de testemunhas (ver caixa) referem que dezenas de pessoas se atiraram à água para tentar escapar ao atirador, que, vestido de polícia, foi até junto da margem e continuou a disparar.
"Não sabemos ainda se agiu sozinho", afirmou um porta-voz da polícia, assegurando que os indícios excluem a possibilidade de os ataques estarem ligados a redes terroristas internacionais.
Não há igualmente certezas sobre o ataque à sede do governo norueguês, não sendo seguro se houve uma ou várias explosões.
Mas sabe-se que a bomba colocada numa carrinha estacionada junto ao prédio onde se situava o gabinete do primeiro-ministro Jens Stoltenberg foi fabricada à base de fertilizante agrícola.
Este indício aponta para Breivik, que em Maio comprou seis toneladas de fertilizante através da companhia Breivik Geofarm.
O fornecedor confirmou a compra e considerou-a "normal para um produtor agrícola comum".
Surgiram entretanto revelações surpreendentes sobre o responsável pelo maior massacre na Noruega desde a Segunda Guerra Mundial.
Breivik criou perfis no Twitter e no Facebook dias antes dos atentados em que se dizia admirador de Churchill e incluiu uma frase significativa: "Um homem de convicções vale mais do que 100 mil só com interesses.
"Crítico do multiculturalismo europeu, Breivick acusa os islâmicos de serem maioritariamente radicais.
Como livros favoritos, referia ‘1984’, de George Orwell, e ‘O Príncipe’, de Maquiavel.
PORTUGUESES REFEREM TRISTEZA E APATIA
"Há uma imensa tristeza.
Isto vai afectar muitas gerações", afirmou à Lusa Nuno Marques (na foto), o único futebolista português na Noruega.
Rui Sales, há 25 anos no país, diz que "as pessoas estão apáticas.
Não percebem a razão de tudo isto".
Outro português referiu, sob anonimato, que "escapou por minutos" à explosão que arrasou a sede do governo, em Oslo: "Foi sorte.
Foi só porque fui buscar os meus filhos mais cedo."
"RIA-SE E GRITAVA VITÓRIA"
"Um paraíso foi transformado num inferno."
Foi assim que o primeiro-ministro da Noruega, Jens Stoltenberg, resumiu o terror vivido por centenas de jovens na ilha de Utoya, onde, na altura do tiroteio, tinha lugar um encontro de jovens do Partido Trabalhista.
Nos seus testemunhos, os sobreviventes descrevem um cenário de pesadelo comparável a um filme de terror.
Erik Kursetgjerde, de 18 anos, contou como tudo começou: "Estava vestido de polícia e pediu às pessoas para se aproximarem.
‘Está tudo bem, estou aqui para vos ajudar’, disse.
Depois, quando cerca de 20 pessoas se aproximaram, disparou à queima-roupa.
"Entre a incredulidade e o pânico, dezenas de jovens começaram então a correr em todas as direcções.
"As pessoas gritavam e imploravam pela vida", acrescentou Erik: "Nessa altura tive a certeza de que ia morrer."
Em desespero, fez o que dezenas de outros fizeram: correu para a água e tentou afastar-se a nado.
Um barco que passava salvou-lhe a vida.
Muitos tentaram escapar fingindo-se mortos, mas Breivik aproximava-se "e disparava um segundo tiro sobre os corpos caídos", contou Dana Berzingi, de 21 anos.
Adrian Pracon, também de 21 anos, escapou por pouco: "Estava deitado de cara para baixo e ouvi-o a aproximar-se.
Deu-me um tiro nas costas, mas felizmente não me mexi."
"Inicialmente matou pessoas na ilha, depois começou a disparar sobre os que estavam na água", contou, por seu lado, Elise, de 15 anos, que se escondeu no lago, sob uma rocha da qual o atirador abriu fogo sobre as pessoas.
"Conseguia ouvi-lo respirar.
Ria-se e dava gritos de vitória", recorda a jovem.

    """
print summarize(content, language='portuguese')


