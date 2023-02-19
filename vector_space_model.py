from flask import Flask, jsonify, request, make_response
import math, glob
from collections import defaultdict
from os import listdir
from os.path import isfile, join
from nltk import word_tokenize
import numpy as np
import json
from datetime import datetime

from pymongo import MongoClient

import traceback
import logging

logging.basicConfig(filename='./logfile/static_information.log', level=logging.DEBUG, format='%(message)s')
logging.info('\n\n\n########################### ' + str(datetime.now()) + ' ###############################')

app = Flask(__name__)

def add_document(doc):
    '''
    Add a document to the inverted index. Returns the document's ID
    '''
    global documents, docid_counter, the_index
    # do not re-add the same document.
    if doc in documents.values():
        print(f'document already included!')
        print(doc)
        return
    docid = docid_counter
    documents[docid] = doc
    docid_counter += 1
    #print("Adding document %s to inverted index with document ID %d" % (doc, docid))
    #print(f"Adding document to inverted index with document ID %d" % (docid))
    '''
    Datastructure storing everyting: 
    {term:{df:scalar,docs:{docid:tf_d}}}
    '''
    for term in word_tokenize(doc):
        # TODO: collect term frequencies and document frequencies per term.
        # new term
        if not term in the_index.keys():
            the_index[term] = {
                'df':1,
                'docs':{
                    docid:1 # tf_d = 1
                }
            }
        
        # term already seen
        else:
            
            # doc already seen
            if docid in the_index[term]['docs'].keys():
                the_index[term]['docs'][docid] += 1
                
            else:
                the_index[term]['docs'][docid] = 1
                the_index[term]['df'] += 1

def fill_dict():
    
    # initialize DB
    db = MongoClient().file_db
    print(f'initialized mongo db: {db}')

    mypath = './data_sources/'
    allfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
    pdffiles = [f for f in allfiles if f.split('.')[-1]=='pdf']
    for filename in pdffiles:
        print(f'document found: {filename}')
        for data in db.documents.find({'filename':filename}):
            print(f'adding document')
            add_document(data['content'])


def tf(term, docid):
    '''
    Calculate term frequency for term in docid. Return 0 if term not in index,
    or term does not appear in document.
    '''
    if docid in the_index[term]['docs'].keys():
        return the_index[term]['docs'][docid]
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
    # TODO: implement
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

def cosine_score(query, K=3):
    '''
    Compute cosine scores for query `query` and return the top K results
    according to Figure 6.14.
    '''
    # Initialize arrays so we can use docids as indices
    scores = [0] * (len(documents.keys())+1)
    length = [0] * (len(documents.keys())+1)
    result = [0] * (len(documents.keys())+1)
    # Precompute length array values -- these are the normalization factors
    for d in documents.keys():
        length[d] = norm_cosine(d)
    print('length array: ', length)
    # TODO: implement
    # 1. compute scores for each document, store in scores array
    for word in word_tokenize(query):
        if word in the_index.keys():
            for document_id in the_index[word]['docs']:
                score = tf_idf(word, document_id)
                print(score)
                scores[document_id] += score
    # 2. Normalize using the length array
    #result = np.array(scores) / np.array(length)
    print(f'scores array {scores}')
    for i in range(1,len(result)):
        result[i] = scores[i]/length[i]
    # 3. Return top-K: sort by descending score and return first K elements of result.
    print(f'result array: {result}')
    top_docs = np.array(result).argsort()[-K:][::-1]
    result = np.array(result)
    result[::-1].sort()
    top_scores = result[:K]
    return list(zip(top_docs, top_scores))

@app.route('/query', methods=['POST'])
#def execute_query(query):
def execute_query():
    '''
    Execute a string query on the vector space model index.
    '''
    # We use the new remove_stop_words helper function to split and normalize
    # the query. After this call query is a list of words to query for
    #query = remove_stop_words(query)
    logging.info("Static information retrieval started")
    #query = request.form['query']
    query = request.get_json()['query']
    logging.info("QUERY: " + str(query))  
    #print(f'User query: {query}')
    tmp = cosine_score(query)
    #print(f'Cosine scores: {tmp}')
    ret = print_result(tmp)
    logging.info(str(ret))
    logging.info("SUCCESSFULL")
    return jsonify(ret)


def print_result(results):
    '''
    Initially used to pretty-print the results. 
    Now used to structure the results. 
    '''
    
    # if not results:
    #     print("No documents found")
    #     return_result = {
    #         "filename": json.loads(0),
    #         "file_url": json.loads(0),
    #         "docid": json.loads(0),
    #         "score": json.loads(0),
    #         "document": json.loads(0)
    #     }
    
    # If we got some results, print them
    # Multiple documents might be accurate, for the beginning we only return the one with the highest score.
    # else:
    print(results)
    docid, score = results[0]
    if score > 0:
        print(docid)
        print(score)
        db = MongoClient().file_db

        found_filename = db.documents.find_one({'content':documents[docid]})['filename']
        file_url = db.files.find_one({'filename':found_filename})['file_url']
        print(f'There is a document in the documents database with the filename: {found_filename} and corresponding url: {file_url}')

        return_result = {
            "filename": found_filename,
            "file_url": file_url,
            "docid": json.dumps(int(docid)),
            "score": json.dumps(float(score)),
            "document": documents[docid]
        }
    else:
        # print("No documents found")
        # return_result = {
        #     "filename": json.loads(0),
        #     "file_url": json.loads(0),
        #     "docid": json.loads(0),
        #     "score": json.loads(0),
        #     "document": json.loads(0)
        # }
        print("No documents found")
        return_result = {
            "filename": '',
            "file_url": '',
            "docid": '',
            "score": '',
            "document": ''
        }


    return return_result

        #for (docid, score) in results:
            #print('%2d(%6.3f) -> %s' % (docid, score, documents[docid]))
            #return_result.append([docid, score,documents[docid]])

   

if __name__ == '__main__':

    '''Map document titles to document ids'''
    documents = {}
    '''A running counter for assigning numerical IDs to documents'''
    docid_counter = 1
    '''The document-term frequencies'''
    the_index = dict()

    fill_dict()
    print(f'code executed')
    app.run(debug=False, host='127.0.0.1', port=5010)

    

