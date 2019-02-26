# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 14:49:18 2019

@author: Rogith
Class InvertedIndex
Ranked Document Retrieval
"""

from bs4  import BeautifulSoup
import nltk
nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string
import re
import operator
import math

ps = PorterStemmer()


#import
printable = set(string.printable)

# Unit Test: try different ways of parsing the documents and seeing what works
# best as far as eliminating unwanted characters. this test will utilize code
# given in campus wire, where they define the set printabe above enabling the
# the use of a lambda function



# function that filters uwantwed characters
def filter_special_char(word):
    sChars = [ '&' , '\x00' ,'\x00\x00' , '\x00\x00\x00' , '\n']

    if(word not in sChars):
        return True
    else:
        return False
        
class InvertedIndex:
    def __init__(self): #input_file, stop_list_set, term_list, term_index, doc_index):
        self.stop_list_set = set()
        self.term_list = list()
        self.term_index = dict()
        self.doc_index = dict()

    #fuction that creates list of stopwords
    def make_stop_list(self, stop_list_file):
        path = stop_list_file
        with open(path) as fp:
            for line in fp:
                for word in line.split():
                    self.stop_list_set.add(word.lower())
    
    def add_term(self, term, doc_name):
        translator = str.maketrans( '' , '' , string.punctuation)
        filtered_term = term.translate(translator)
        x = (filtered_term, doc_name)
        self.term_list.append(x)
    
    
    #function that creates termlist and doc_idx as we count each doc_length
    def make_term_list_and_doc_index(self, file_name):
        dash = '-'
        http = 'http'
        soup = BeautifulSoup(open(file_name), 'lxml')
        for doc in soup.find_all('doc'):
            for doc_i in doc.find_all('docno'):
                #single_doc = doc_i.text.strip().split(' ')
                single_doc = doc_i.text.split()
                #single_doc = doc_i.text.read()
                doc_name = single_doc[0] # why element 0?
                for txt in doc.find('text'):  
                    #words = filter(filter_special_char, txt.strip().split(' '))
                    #print(txt)
                    terms = word_tokenize(txt)
                    #print(terms)
                    #words = filter(filter_special_char, txt.split())
                    words = filter(filter_special_char, terms)
                    
                    #words = word_tokenize(terms)
                    count = 0
                    for w in words:
                        w = w.lower()
                        word = ps.stem(w)
                        if word not in self.stop_list_set:
                            # check if '-' in word and 'http' not in word
                            if re.search(dash, word) and not re.search(http, word):
                                #replace dash with a space
                                word_set = word.replace("-"," ")
                                #parse each word
                                for term in word_set.split():
                                    count += 1
                                    self.add_term(term, doc_name)
                            else:
                                count += 1
                                self.add_term(word, doc_name)
                self.doc_index[doc_name] = count
                                
                    
    def update_term(self, item):
        i = 0
        for listitem in self.term_index[item[0]]:
            #if word_docName == encounterd_fileID
            if (item[1] == listitem[0]):
                listitem[1] += 1
                return
            else:
                i += 1
        self.term_index[item[0]].append( [item[1] , 1 ] )
        return
    
        
    def make_term_index(self):
        for item in self.term_list:
            if item[0] not in self.term_index:
                # add term
                two_elem_list = [item[1], 1]
                new_list = [two_elem_list]
                self.term_index[item[0]] = new_list
            else:
                # update term
                self.update_term(item)
    
    
    def get_term_data(self, term):
        print(term + '-> ')
        if term in self.term_index:
            for postings in self.term_index[term]:
                tf = postings[1]/self.doc_index[postings[0]] #num_occur/doc_size
                idf = math.log(len(self.doc_index)/len(self.term_index[term]), 2)
                tf_idf = tf*idf
                print('for this posting: Doc#' + str(postings[0]) + ', tf: ' + str(tf) + ', idf: ' + str(idf) + ', tf-idf: ' + str(tf_idf))
        else:
            print('Term not found')
        
    def get_posting_list(self, term):
        #trm = term.stemming
        if term in self.term_index:
            return self.term_index[term]
        else:
            postings = list()
            return postings
        
    def get_q_weight(self, term, query_words):
        tf = 0
        for w in query_words:
            if w.lower() == term:
    	        tf += 1
        tf = tf / len(query_words)
        t = ps.stem(term)
        if t in self.term_index:
            idf = 1 + math.log(len(self.doc_index)/len(self.term_index[t]))
        else:
            idf = 1
    	
        return tf * idf
    
    def get_d_weight(self, term, pair):
    	if term in self.term_index:
    		#postings = self.term_index[term]
    		tf = pair[1]/self.doc_index[pair[0]] #num_occur/doc_size
    		idf = 1 + math.log(len(self.doc_index)/len(self.term_index[term]))
    		tf_idf = tf * idf
    	else:
    		tf_idf = 0
    	return tf_idf

    #end class

def cosine_score(query_words, inv_idx):
    scores = dict()
    for doc in inv_idx.doc_index.keys():
        scores[doc] = 0
        
        
    #query_words = query.split()
    
    for t in query_words:
        t = t.lower()
        if t not in inv_idx.stop_list_set:    
            term = ps.stem(t)
            postings = inv_idx.get_posting_list(term)
            q_t_weight = inv_idx.get_q_weight(t, query_words)
            
            
            for pair in postings:
                d_t_weight = inv_idx.get_d_weight(term, pair)
                scores[pair[0]] += q_t_weight * d_t_weight
        
    for doc in inv_idx.doc_index.keys():
        scores[doc] = scores[doc] / inv_idx.doc_index[doc]
        
    sorted_scores = sorted(scores.items(), key = operator.itemgetter(1), reverse = True)
    return sorted_scores



# code resembling main function/driver
inv_idx = InvertedIndex()
inv_idx.make_stop_list('stoplist.txt')
inv_idx.make_term_list_and_doc_index('ap89_collection')
inv_idx.make_term_index()
termIndex = inv_idx.term_index
docIndex = inv_idx.doc_index

translator = str.maketrans( '' , '' , string.punctuation)
path = 'query_list.txt'
q_nums = list()
queries = dict()

#load queries and load q_num
#each query word is now its own element in a list
with open(path) as fp:
    for line in fp:
        q_num_flag = True
        for word in line.split():
            filtered_term = word.translate(translator)
            if q_num_flag:
                q_nums.append(filtered_term)
                queries[q_nums[-1]] = []
                q_num_flag = False
            else:
                
                queries[q_nums[-1]].append(filtered_term)

scores_list = dict()

for q in queries.keys():
    scores = cosine_score(queries[q], inv_idx)
    scores_list[q] = scores
    
f = open("results_file.txt","w+")

for q in scores_list.keys():
    q_num = q
    count = 1
    for list_l in scores_list[q]:
        doc_name = list_l[0]
        if list_l[1] > 0:
            f.write(str(q) + ' Q0 ' + doc_name + ' ' + str(count) + ' '+ str(list_l[1]) +' Exp\n' )
            count += 1

f.close()
