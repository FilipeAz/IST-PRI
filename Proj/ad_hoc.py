import re
import string
from nltk.corpus import stopwords
import gensim.summarization.bm25 as BM25
from doc_retrieval import *


def create_corpus(lst):		#puts corpus in a list, each position is a list 
	
	corpus = []	

	for i in lst:
		text = get_text(i)
		title = get_title(i)
		st = text + title
		aux_text = st.split()
		corpus = corpus + [aux_text]

	return corpus 	

# query stats
def num_manifestos_party(res, query, text): 
	dict = {} # number of results by each party
	keywords = {} # dict with keywords of query
	
	for el in query:
		keywords.update({el: []})
		
	for [rel, title, party] in res:
		if party not in dict:
			dict.update({party : 1})
		else:
			dict[party] += 1

	for el in dict:
		line = el + ": " + str(dict[el])
		print (line)
	return dict.keys()

def show_status(res, query, text, lst_keywords):
	
	dic = {}
	dic_aux = {}
	for el in res:
		print(el)

	print("\n\n\n")		
	print("Statistics about keywords:\n")
	print("party — number of manifestos: \n ")	
	key_party = num_manifestos_party(res, query, text)	
	print( "--------------------------------- \n")
	print("Return a list that calculates how many times each party mentions each keyword:")
	for l in lst_keywords:
		if l[0] in key_party:
			st = 'party: ' + l[0] + '\tword :' + l[1] + '\tcount: ' + str(l[2])
			print(st)
			if l[0] in dic:
				dic[l[0]][0] += 1
				dic[l[0]][1] += l[2]

			else:
				dic.update({l[0] : [1, l[2]]})	
			
	print("----------------------------------- \n")	
	print("Return a party and the number of keywords appeared on this party:")
	for key, value in dic.items():
		print(key, value[0])
	print("----------------------------------- \n")	
	print("Return a total count of keywords on a party")
	for key, value in dic.items():
		print(key, value[1])
		


def calculate_stats(lst, query):

	lst_keywords = []

	for i in lst:
		
		for j in query:

			tag = False	

			word_count = get_text(i).count(j) # number of keywords in a document
			if word_count != 0:

				if lst_keywords == []:
					lst_keywords = [[get_party(i), j, word_count]] #list that contains the party, query and the number of times the query appears in that party's document

				for l in lst_keywords:
					if l[0] == get_party(i) and l[1] == j:
						l[2] += word_count
						tag = True	

				
				if tag == False:		
					lst_keywords = lst_keywords + [[get_party(i), j, word_count]] #list that contains the party, query and the number of times the query appears in that party's document
					
	return lst_keywords
					

def calculate_BM25(keywords, lst):	#calculates the BM25 weights

	maxweight = -1000
	results = []


	stopWords = set(stopwords.words('portuguese'))
	for i in range(len(keywords)): 
		keywords[i] = keywords[i].lower()
	
	new_keywords = [word for word in keywords if word not in stopWords]
	#print(new_keywords)


	corpus = create_corpus(lst)
	#print(corpus)

	bm25 = BM25.BM25(corpus)
	average_idf = sum(float(val) for val in bm25.idf.values()) / len(bm25.idf)	#average idf
	#print(average_idf)
	
	scores = bm25.get_scores(new_keywords, average_idf)		#bm25 scores
	#print(scores)	

	for i in range(len(scores)): 
		if scores[i] != 0:
			results = results + [[scores[i], get_title(lst[i]), get_party(lst[i])]]		#different than 0 scores

	results.sort(key=lambda document: document[0], reverse=True)	#most relevant ones
	
	return results, new_keywords
		













