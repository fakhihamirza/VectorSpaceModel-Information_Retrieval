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

def Pre_processing():
    #for all documents in corpus-open file and read
    # f= open("stemmed.txt", "w")
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
        stemmed_tokens=[ps.stem(word) for word in tokens]
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
                    Index[word]['tf'][doc_num -1 ] = Index[word]['tf'][doc_num -1 ] +1
                Index[word]['idf'] = math.log(total_documents/(Index[word]['df']))     #formula is log(N/df) not log(df/N)
                Index[word]['tf-idf'][doc_num -1 ] = Index[word]['tf'][doc_num -1] * Index[word]['idf']


# Writing indexes to file
def write_to_file():
    f = open("Index.txt","w")
    f.write( str(Index) )
    f.close()

Pre_processing()
write_to_file()