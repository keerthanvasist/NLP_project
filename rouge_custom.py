import sys
from os import path, walk
from math import exp
import operator

reload(sys)
sys.setdefaultencoding('utf8')


def computeCount(data,n):
	words = str(data).lower().strip().split()
	ngramDict = buildCountDictionary(words,len(words) - n + 1,n)
	return ngramDict, len(words) - n + 1, len(words)


def buildCountDictionary(words,limits,n):
	wordDict = {}
	for i in range(0,limits):
		ngram = ' '.join(words[i:i+n])
		if ngram not in wordDict.keys():
			wordDict[ngram] = 1
		else:
			wordDict[ngram] += 1
	return wordDict

def computeClipCount(candidateDict, referenceDict):
	clipCount = 0
	for key in candidateDict.keys():
		CandidateCount = candidateDict[key]
		maxReferenceCount = 0
		# for ref in referenceCount:
		if key in referenceDict:
			maxReferenceCount = max(referenceDict[key],maxReferenceCount)
		CandidateCount = min(maxReferenceCount, CandidateCount)
		clipCount += CandidateCount

	return clipCount


def getNGramPrecision(n=2):
	clipCount = count = r = c = 0

	referenceDict, refCount, referenceLength = computeCount(referenceData, n)

	candidateDict, newCount, candidateLength = computeCount(candidateData, n)

	clpCount = computeClipCount(candidateDict, referenceDict)

	clipCount += clpCount
	count += newCount

	if clipCount != 0:
		recall = float(clipCount) / count
	else:
		recall = 0

	return recall


def getNGramRecall(n=2):
	clipCount = count = r = c = 0

	referenceDict, refCount, referenceLength = computeCount(referenceData, n)

	candidateDict, newCount, candidateLength = computeCount(candidateData, n)

	clpCount = computeClipCount(candidateDict, referenceDict)

	clipCount += clpCount
	count += refCount

	if clipCount != 0:
		recall = float(clipCount) / count
	else:
		recall = 0

	return recall


# with open('article.txt', 'r') as fp:
# 	referenceData = fp.read()

# with open('out.txt', 'r') as fp:
# 	candidateData = fp.read()

def run_evaluation(refData,candData):
	global referenceData, candidateData
	referenceData = refData
	candidateData = candData
	rouge = getNGramRecall(2)
	bleu = getNGramPrecision(2)
	fScore = 2 * rouge * bleu / (rouge + bleu)

	# print "Rouge Score = " + str(rouge)
	# print "Bleu Score = " + str(bleu)
	# print "F Score = " + str(fScore)
	# print "\n\n\n"
	return rouge

