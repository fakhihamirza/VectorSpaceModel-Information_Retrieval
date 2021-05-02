import nltk
import string
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import os
import sys
import ast
import math

stopwords_file = open('Stopword-List.txt', errors="ignore").read()
stopwords = nltk.word_tokenize(stopwords_file)

stemmed_tokens=[]
Index = {}
ps = PorterStemmer()
total_documents = 50
q_vector = {}
all_words =[]

def Pre_processing():
    #for all documents in corpus-open file and read
    for doc_num in range(1,(total_documents+1)):
        file_name = str(doc_num) + ".txt"
        content = open(file_name,"r",encoding = "utf-8", errors="ignore").read()
        content=content.lower()      #TO LOWER
        #Remove punctuations and tokenize
        regex = re.compile('[^a-zA-Z0-9\s]')
        content = re.sub(regex,' ',content)
        regex = re.compile('[-]')
        content = re.sub(regex,' ',content)
        tokens = nltk.word_tokenize(content)
        #Stemming
        # stemmed_tokens=[ps.stem(word) for word in tokens]
        stemmed_tokens = tokens
        all_words.extend(stemmed_tokens)
        #Creating Index
        word_position = 0
        for word in stemmed_tokens:
            if word not in stopwords:
                if word not in Index:
                    Index[word]={
                        'tf' : [0]*total_documents,  #list of termfreq for each doc
                        'df' : 0,
                        'idf':0,
                        'tf-idf':[0]*total_documents  # list of tf-idf for each doc
                    }
                    Index[word]['tf'][doc_num-1] = 1
                    Index[word]['df'] = 1
                else :
                    if Index[word]['tf'][doc_num -1] == 0 :  #found in new doc
                        Index[word]['df'] = Index[word]['df'] + 1
                        Index[word]['tf'][doc_num-1] = 1
                    else :
                        Index[word]['tf'][doc_num -1 ] = Index[word]['tf'][doc_num -1 ] +1 

    for doc_num in range(1,(total_documents+1)):
        for word in Index:
            Index[word]['idf'] = math.log(total_documents/(Index[word]['df']) , 10 )     #formula is log(N/df) not log(df/N)
            Index[word]['tf-idf'][doc_num -1 ] = Index[word]['tf'][doc_num -1] * Index[word]['idf']

# Writing index and q_vector to file
def write_to_file():
    f = open("Index.txt","w")
    f.write( str(Index) )
    f.close()

    f = open("Query_vector.txt","w")
    f.write( str(q_vector) )
    f.close()

    with open("words.txt", 'w') as f:
        for s in all_words:
            f.write(s + '\n')

def read_from_file():
    file = open("Index.txt","r")
    contents = file.read()
    Index=ast.literal_eval(contents)
    print(type(Index))
    file.close()

    
    with open("words.txt", 'r') as f:
        all_words = [line.rstrip('\n') for line in f]
    # return all_words
    

def query_vector(query):
    query=query.lower() 
    regex = re.compile('[^a-zA-Z0-9\s]')
    query = re.sub(regex,' ',query)
    regex = re.compile('[-]')
    query = re.sub(regex,' ',query)
    q_list = nltk.word_tokenize(query)  

    q_tokens=q_list

    print (q_tokens)

    for word in all_words:
        if word not in stopwords:
            if word not in q_vector:
                q_vector[word] = 0
            else:                
                if word not in q_tokens:
                    q_vector[word] =0
                else:
                    q_vector[word] = 1   # using 0 1 method for query else use below formula
                    # (q_tokens.count(word) * Index[word]['idf'])  # multiplying term freq in query * idf of word

res = []

def vsm(alpha):
    x = 0.0
    a = 0.0
    b = 0.0
    final = []
    for doc_num in range(1,51):
        for word in q_vector:
            if word not in stopwords:
                x += (q_vector[word] * Index[word]['tf-idf'][doc_num -1])  #index is doc is word tf-idf
                a += q_vector[word]**2
                b += Index[word]['tf-idf'][doc_num -1]**2
        res.append(x / (math.sqrt(a) * math.sqrt(b) ) )
        x = 0.0
        a = 0.0
        b = 0.0
    print(res)
    doc = []
    f=1
    for i in res:
        if i > alpha:
            final.append(i)
            doc.append(f)
        f = f +1
    return final, doc

# Pre_processing()
# q = input()
# alpha = input()
# query_vector(q)
# write_to_file()
# # print(q_vector)
# print(vsm(float(alpha)))

def start(query):
    Pre_processing()
    alpha = 0.005
    query_vector(query)
    return vsm(float(alpha))