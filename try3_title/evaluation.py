from glob import glob
import re,math
from itertools import tee, islice
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
directory_output_main = "outputSummaries/PriberamCompressiveSummarizationCorpus"
directory_main = "PriberamCompressiveSummarizationCorpus"

def createNgrams(n,sentence):
  # print lst
  tempsentence = sentence
  while True:
    # print a,b
    a, b = tee(tempsentence)
    temp_tuple = tuple(islice(a, n))
    # print temp_tuple
    if len(temp_tuple) != n:
        # print "n not equal"
      break
    else:
      yield temp_tuple
      next(b)
      tempsentence = b
def returnBleuScore(cntr_candidate,cntr_reference,referencelist):
    bleuscore = 0
    for w in cntr_candidate:
            
        candidate_count = cntr_candidate[w]
        max_count = -99
            
        for i in range(0,len(referencelist)):
            temp_count = cntr_reference[i][w]
                
            if(temp_count > max_count):
                max_count = temp_count
                
        if candidate_count >= max_count:
            final = (max_count * 1.0)
        else:
            final = (candidate_count * 1.0)
            
        bleuscore += final
    return bleuscore
def returnMinLen(rlens,temp_r_value,cntr_line,cntr_reference,cntr_candidate,ngram,referencelist):
    minr = sys.maxint
    minlen = sys.maxint
    for i in range(0,len(referencelist)):
        temp_r_value = sys.maxint
        l = referencelist[i]
        line = l[cntr_line]
        line = createNgrams(ngram,line.split())
        temp = []
        for word in line:
            temp.append(word)
        temp_counter = Counter(temp)
        templen = sum(temp_counter.values())
        temp_r_value = abs(sum(cntr_candidate.values())-templen)
        if minr > temp_r_value:
            minr = temp_r_value
            minlen = templen
        cntr_reference.append(temp_counter)
        rlens[i] += templen
    return minlen


def calculate_BP_bleu(ngram,referencelist):
    rlens=[0]*len(referencelist)
    
    # print "*********"
    # print len(rlens)
    r_value = 0
    temp_r_value = 0
    totalwords = 0
    cntr_line = 0 
    bluescore_answer = 0
    
    for sentence_candidate in candidatelist:
        cntr_reference = []
        cntr_candidate = []
        sentence_candidate = createNgrams(ngram,sentence_candidate.split())
        temp = []
        for word in sentence_candidate:
            temp.append(word)
        cntr_candidate = Counter(temp)
        totalwords += sum(cntr_candidate.values())
        
        minr=0
        
        if sum(cntr_candidate.values())==0:
            cntr_line += 1 
            continue
       
        r_value += returnMinLen(rlens,temp_r_value,cntr_line,cntr_reference,cntr_candidate,ngram,referencelist)
        
        cntr_line += 1  
        
        bluescore_answer += returnBleuScore(cntr_candidate,cntr_reference,referencelist)
    if(totalwords==0):
        bluescore_answer = 0
    else:
        bluescore_answer = bluescore_answer/totalwords
    if ngram==1:
        return bluescore_answer,totalwords,r_value 
    else:
        return bluescore_answer
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

	
	

system_topicwise_summaries = combine_system_summaries(directory_output_main)
human_topicwise_summaries = combine_human_summaries(directory_main)

for key in system_topicwise_summaries:
	print key
	print system_topicwise_summaries[key]
	print human_topicwise_summaries[key]
	break
	# bleu=[0]*4
	# bleu_intermediate = 0
	# candidatelist = system_topicwise_summaries[key]
	# referencelist = human_topicwise_summaries[key]
	# bleu[0],c1,r1=calculate_BP_bleu(1,referencelist)
	# bleu[1]=calculate_BP_bleu(2,referencelist)
	# bleu[2]=calculate_BP_bleu(3,referencelist)
	# bleu[3]=calculate_BP_bleu(4,referencelist)
	# if c1==0:
	#     bp = 0
	# else:
	#     if c1 <= r1:
	#         bp = math.exp(1 - 1.0 * r1 / c1)
	#     else:
	#         bp = 1
	# for i in range(0,4):
	#     if bleu[i]!=0:
	#         bleu_intermediate += log(bleu[i])
	# # print bleu_intermediate        
	# bleu_ans = bp * (math.exp((0.25) * (bleu_intermediate)))

	# print "topic no."+key
	# print bleu_ans
