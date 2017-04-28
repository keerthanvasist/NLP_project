
from glob import glob
import re,math
from nltk.corpus import stopwords
import sys
import heapq
import os,errno
from collections import Counter


reload(sys)
sys.setdefaultencoding('utf8')
stop = stopwords.words('portuguese')
folder_year = ['/PT2010-2011','/PT2012-2013']
folder_type = "/docs"
directory_main = "PriberamCompressiveSummarizationCorpus"
def get_cosine(vec1, vec2):
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])
	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)
	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator

def sentence_to_vector(line,tf_map):
	sentence_vector = {}
	words = line.split()
	tf_idf_sum = 0
	sentence_length = 0
	for word in words:
		if word in tf_map:
			sentence_length += 1
			sentence_vector[word] = tf_map[word]
	return sentence_vector
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


articles_corpus = makelist(directory_main)
idf_map = {}
# print "one"
for article in articles_corpus:
	actual_article = article[0]
	lines = actual_article.split()
	for word in lines:
		if word not in stop:
			idf_map[word] = 0

#code to create the idf map
for key in idf_map:
	for article in articles_corpus:
		
		if key in article[0]:
			idf_map[key] += 1
for key in idf_map:
	idf_map[key] = math.log(801*1.0/(1+idf_map[key]))
# for all the articles

for article in articles_corpus:

	lines = article[0].split()
	tf_map = {}
	for word in lines:
		if word not in stop:
			if word not in tf_map:
				tf_map[word] = 0
			else:
				tf_map[word] += 1
	for key in tf_map:
		tf_map[key] = tf_map[key] * 1.0 * idf_map[key]
	#for each sentence calculate the tf-idf score
	lines = article[0].split('\n')
	# separate the headline from the article
	headline_vector = sentence_to_vector(lines[0],tf_map)
	lines = lines[1:]
	sentence_dict = {}
	for line in lines:
		sentence_vector = sentence_to_vector(line,tf_map)
		sentence_dict[line] = get_cosine(headline_vector, sentence_vector)
		
	
	filename = "outputSummaries/"+article[1]+"_summary_cosine.txt"
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	output = heapq.nlargest(3, sentence_dict, key=sentence_dict.get)
	with open(filename, "w") as f:
		f.write(output[0]+"\n"+output[1]+"\n"+output[2])
	


		
