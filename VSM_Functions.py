import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

import pickle

from nltk import word_tokenize

import numpy as np
import json

import math
import string


# Notwendige Datensätze
with open('./data/the_index_stem.pickle', 'rb') as handle:
    the_index = pickle.load(handle)

with open('./data/documents.pickle', 'rb') as handle:
    documents = pickle.load(handle)

with open('./data/docid_counter.pickle', 'rb') as handle:
    docid_counter = pickle.load(handle)

with open('./data/games_reviewed.pickle', 'rb') as handle:
    games_reviewed = pickle.load(handle)

with open('./data/unique_tags.pickle', 'rb') as handle: 
    unique_tags = pickle.load(handle)


def tf(term, docid):
    '''
    Calculate term frequency for term in docid. Return 0 if term not in index,
    or term does not appear in document.
    '''
    if docid in the_index[term]['docs'].keys():
        return 1+math.log(the_index[term]['docs'][docid])
    else:
        return 0 

def df(term):
    '''
    Extract frequency of term for document with id docid from index
    '''
    if term in the_index.keys():
        return the_index[term]['df']
    else:
        return 0

def idf(term):
    '''
    Compute idf_t for a term
    '''
    df_t = df(term)
    return math.log(docid_counter/df_t)

def tf_idf(term, docid):
    '''
    Compute tf-idf for term and docid
    '''
    return tf(term,docid)*idf(term)

def norm_cosine(docid):
    '''
    Compute cosine normalization for docid
    '''
    sos = 0
    for term in the_index.keys():
        if docid in the_index[term]['docs'].keys():
            sos += tf_idf(term,docid)**2
    return math.sqrt(sos)

def cosine_score(query, K=47):
    '''
    Compute cosine scores for query `query` and return the top K results
    '''
    # Initialize arrays so we can use docids as indices
    scores = [0] * (len(documents.keys())+1)
    length = [0] * (len(documents.keys())+1)
    result = [0] * (len(documents.keys())+1)
    # Precompute length array values -- these are the normalization factors
    for d in documents.keys():
        length[d] = norm_cosine(d)

    # Stemming & Stopword
    stemmer = SnowballStemmer("english")
    stop = stopwords.words('english') + list(string.punctuation) + ['\n']
    for word in word_tokenize(query.lower().strip()):
        if word in stop:
            continue
        else:
            word = stemmer.stem(word)
            if word in the_index.keys():
                for document_id in the_index[word]['docs']:
                    score = tf_idf(word, document_id)
                    print(score)
                    scores[document_id] += score

    # 2. Normalize using the length array
    for i in range(1,len(result)):
        result[i] = scores[i]/length[i]

    # 3. Return top-K: sort by descending score and return first K elements of result.
    # print(f'result array: {result}')
    top_docs = np.array(result).argsort()[-K:][::-1]
    result = np.array(result)
    result[::-1].sort()
    top_scores = result[:K]
    return list(zip(top_docs, top_scores))


def print_result(results, df, tag, top = 10):    

    game_list = []
    review_count_list = []
    recommendation_ratio_list = []
    avg_playtime = []
    tag_list = []
    for i in range(1,1+len(results)):

        docid, score = results[i-1]
        if score > 0:


            game_list.append(df[df["docid"] == docid]["title"].values[0])
            review_count_list.append(df[df["docid"] == docid]["review_count"].values[0])
            recommendation_ratio_list.append(df[df["docid"] == docid]["recommendation_ratio"].values[0].round(2)*100)
            avg_playtime.append(df[df["docid"] == docid]["avg_playtime"].values[0].round(2))
            tag_list.append(df[df["docid"] == docid]["tags"].values[0])
            


        else:

            game_list.append('No Results')
            review_count_list.append('No Results')
            recommendation_ratio_list.append('No Results')
            avg_playtime.append('No Results')
            tag_list.append('No Results')
            break
    

    result_df = pd.DataFrame({'title': game_list, 'review_count': review_count_list, 'recommendation_ratio': recommendation_ratio_list, 'avg_playtime': avg_playtime, 'tags': tag_list})

    exists = []
    for j in range(0,len(result_df['tags'])):
        # print(result_df['tags'][j])
        exists.append(tag in result_df['tags'][j])
    
    result_df['tag_exists'] = exists

    result_df_final = result_df[result_df['tag_exists'] == True].head(top).reset_index(drop=True)


    return result_df_final