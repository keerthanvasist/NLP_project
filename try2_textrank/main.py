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
	for fold in (dir + f + "/docs" for f in folder_year):
		paths = glob(fold+"/*/")
		for folder in paths:
			folder = folder + "*.sents"
			files = glob(folder)
			for file in files:

				fp = open(file,'r')
				article = []
				article.append(fp.read())
				article.append(file)
				articles_list.append(article)
	return articles_list
def summary_write(articles_list):
	for article in articles_list:
		filename = "outputSummaries/"+article[1]+"_summary_rank.txt"
		if not os.path.exists(os.path.dirname(filename)):
			try:
				os.makedirs(os.path.dirname(filename))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		output = summarize(article[0], language = 'portuguese')
		with open(filename, "w") as f:
			f.write(output)

articles_list = makelist(directory_main)
summary_write(articles_list)


