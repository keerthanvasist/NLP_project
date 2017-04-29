from glob import glob
import re,math
from itertools import tee, islice
from nltk.corpus import stopwords
import sys
import nltk
import heapq
import os,errno
from collections import Counter
# import calculatebleu as bleuscore

reload(sys)
sys.setdefaultencoding('utf8')
stop = stopwords.words('portuguese')
folder_year = ['/PT2010-2011','/PT2012-2013']
folder_type = "/docs"
directory_output_main = "outputSummaries/PriberamCompressiveSummarizationCorpus"
directory_main = "PriberamCompressiveSummarizationCorpus"


def combine_system_summaries(dir):
	topicwise_summaries = {}
	for fold in (dir + f + "/docs" for f in folder_year):
		# print fold
		paths = glob(fold+"/*/")
		for folder in paths:
			
			temp1 = folder[:-1]
			topic_number = temp1[-2:]
			# print topic_number
			folder = folder + "*.txt"
			files = glob(folder)
			summary = []
			for file in files:

				fp = open(file,'r')
				# article = []
				# article.append(fp.read())
				# article.append(file)
				# articles_list.append(article)
				summary.extend(fp.readlines())
				fp.close()
			topicwise_summaries[topic_number] = summary
	return topicwise_summaries

def combine_human_summaries(dir):
	topicwise_summaries = {}
	# print "inside"
	for fold in (dir + f + "/summaries" for f in folder_year):
		# print fold
		paths = glob(fold+"/*.*")

		for path in paths:
			filename = path
			path = path[:-2]
			path = path[-2:]
			# print path
			if path not in topicwise_summaries:
				topicwise_summaries[path] = []
			
			fp = open(filename,'r')
			templist = []
			templist = fp.readlines()
			topicwise_summaries[path].append(templist)
			fp.close()

		
	return topicwise_summaries

	
	
methods = ["try1_tfidf","try3_title"]
for method in methods:
	directory_output_main_temp = method + "/"+directory_output_main
	system_topicwise_summaries = combine_system_summaries(directory_output_main_temp)
	human_topicwise_summaries = combine_human_summaries(directory_main)
	BLEUscore = 0
	count = len(system_topicwise_summaries)
	for key in system_topicwise_summaries:
	    # print key
	    temp = nltk.translate.bleu_score.sentence_bleu(human_topicwise_summaries[key], system_topicwise_summaries[key])
	    if temp != 0:
	    	BLEUscore += temp
	    else:
	    	count -= 1
	print "Average BleuScore for the assessment of "+method+" is:"
	print 1.0 * BLEUscore/count
	# print len(system_topicwise_summaries)
	    # bleuscore.calculate_bleu(system_topicwise_summaries[key],human_topicwise_summaries[key])
	    # break	