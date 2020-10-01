import spacy
from spacy.tokens import Doc
from spacy.lang.pt.examples import sentences
from doc_retrieval import *
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import *
from pprint import pprint
from spacy import displacy
from collections import Counter
import en_core_web_sm


def get_parties(df):

	df = df.drop(df.index[0])

	lst_parties = []

	grouped = df.groupby('party')

	for name, group in grouped:
		lst_parties.append(name)

	return(lst_parties)


def getstats(filename):

	all_entities_dic = {}	# dictionary with the global counter of entities

	dic = {}	# dictionary where each key is a party and each value is a dictionary of entities countings

	lst = ["CARDINAL", "ORDINAL", "TIME", "DATE", "PERCENT", "MONEY", "QUANTITY", "PRODUCT"] # tags that are not relevant

	df = pd.read_csv(filename, sep=',', names=["text","manifesto_id","party","date","title"])

	df = df.drop(df.index[0])

	df_aux = df.groupby(['manifesto_id', 'party', 'date', 'title'])["text"].agg(lambda col: ' '.join(col)) # collapse texts
	
	df_aux = df_aux.reset_index(drop = False)

	lst_parties = get_parties(df_aux) # determine all party authors


	for index, row in df_aux.iterrows():

		nlp = en_core_web_sm.load()

		doc = nlp(row["text"])

		
		entities  = [(X.text, X.label_) for X in doc.ents]
		
		party = df_aux.loc[index]["party"]

		
		if party not in dic:

			dic.update({party : {} })

		for i in entities:

			if i[1] not in lst and i[0] != ' ':

				if i[0] not in dic[party]:

					dic[party].update({i[0] : 1})

				else:

					dic[party][i[0]] += 1 
					
				if i[0] not in all_entities_dic:

					all_entities_dic.update({i[0] : 1})

				else:

					all_entities_dic[i[0]] += 1 


	
	print("---------------------------------------------------------------------")
	print("---------------------------------------------------------------------")
	print("\n")
	print("\tSTATISTICS:")
	print("\n")
	print("---------------------------------------------------------------------")
	print("---------------------------------------------------------------------")
	print("\n")

	party_mentions_by_others = {}	#dictionary where each key is a party and the corresponding value is the number of times they are mentioned by other parties
	

	for party in lst_parties:	#initialization of party_mentions_by_others 
	
		party_mentions_by_others.update({party: 0})


	for i in dic.keys():
		
		#-----------------------------------------------------------------------#
		#What are the most mentioned entities for each party
	
		most_common_ent = []		#list with most common entities
	
		most_common_ent = Counter(dic[i]).most_common(3)

		print(i + "'s most common entities:")
		print("---------------------------------------")
		print(most_common_ent)
		print("\n")
		
		#-----------------------------------------------------------------------#  
		#How many times does any given party mention other parties
		
		for party in lst_parties:
			if party != i:	#other party
				if party in dic[i]:	#is mentioned
					party_mentions_by_others[party] += dic[i][party]
		
		print(i + "'s number of other party mentions:")
		print("---------------------------------------")
		print(sum(party_mentions_by_others.values()))
		print("\n")
		print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		print("\n\n")
		
	
	#-----------------------------------------------------------------------#  
	#What are the most mentioned entities globally(10 most common)
		
	print("Globally most common entities:")
	print("---------------------------------------")
	print(Counter(all_entities_dic).most_common(10))
	print("\n")
		
	#-----------------------------------------------------------------------#  
	#Which party is mentioned more times by the other parties
		
	print("Party is mentioned more times by the other parties (party, nr of mentions):")
	print("---------------------------------------")
	print(Counter(party_mentions_by_others).most_common(1))
	print("\n")
		

				 

		

		


	

