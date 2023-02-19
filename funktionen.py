import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
# nltk.download('stopwords')

import numpy as np
import re

import operator

# Erstellen und Rückgabe eines einfachen Index
# Dokumente sollen tokenisiert und die tokens von nicht Buchstaben gesäubert und in Kleinschreibung umgewandelt werden: z.B. ['abwarten', 'und', 'tee', 'trinken']
def indexCorpus(corpus):
    stemmer = SnowballStemmer('english')
    index = []
    for line in corpus:
        linei = []
        items = line.split(' ')
        for item in items:
            itemt = re.sub(r'\W+', '', item).lower()
            if itemt not in stopwords:
                itemts = stemmer.stem(itemt)
                linei.append(itemts)
        index.append(linei)
    return index

# Berechnung und Rückgabe des Rangierungsscore Nr 1
# Je mehr Suchbegriffe in einem Dokument vorkommen, desto relevanter ist das Dokument.
def calculateScore1(index, query):
    scores = []
    qterms = query.split(' ')
    for ind in index:
        score = 0
        for t in qterms:
            for dt in ind:
                if t == dt:
                    score = score + 1
                    break
        scores.append(score)
    return scores

# Berechnung und Rückgabe des Rangierungsscore Nr 2
# Je haeufiger die Suchbegriffe in einem Dokument vorkommen, desto relevanter ist das Dokument.
def calculateScore2(index, query):
    scores = []
    qterms = query.split(' ')
    for ind in index:
        score = 0
        for t in qterms:
            for dt in ind:
                if t == dt:
                    score = score + 1
        scores.append(score)
    return scores

# Berechnung und Rückgabe des Rangierungsscore Nr 3
# Je frueher ein Suchbegriff in einem Dokument vorkommt, desto relevanter ist das Dokument. Maximal Score ist 10.0.
def calculateScore3(index, query):
    scores = []
    qterms = query.split(' ')
    for ind in index:
        score = 10.0
        for t in qterms:
            for pos, dt in enumerate(ind):
                if t == dt:
                    if pos < score:
                        score = pos + 1
                    break
        fsc = 10.0 / (score)
        scores.append(max(1.0, fsc))
    return scores

# Berechnen aller 3 Rangierungsscores zwischen der Query und den Dokumenten. Der finale Score wird durch die Multiplikation aller 3 Scores berechnet.
def calculateScores(index, query):
    tmp = [calculateScore1(index, query), calculateScore2(index, query), calculateScore3(index, query)]
    final_scores = {}
    for p, ind in enumerate(index):
        final_scores[p] = tmp[0][p] * tmp[1][p] * tmp[2][p]
    return final_scores


# Erstellen des Rankings und Ausgabe der topn Sprichwoerter mit dem jeweiligen Score.
def evaluateScores(scores, corpus, topn):
	sorted_x = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
	topnitems = sorted_x[0:topn]
	result = ''
	for item in topnitems:
		if item[1] > 0.0:
			result = result + '\n' + corpus['title'][item[0]].strip() + ' --> Score: ' + str(item[1])
	return result