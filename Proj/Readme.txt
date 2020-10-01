# PRI
Information Processing and Retrieval Project

Group number 90:
82433 - Ana Nogueira
82468 - Filipe Azevedo
82517 - Martim Zanatti

Requirements:
	Python 3
	Library NLTK
	Library Gensim
	Library Numpy
	Library Pandas
	Library Sklearn
	Library Spacy

To run the code:
- Ad-hoc search:
>> python main.py '1' query(e.g. Partido Politico) 

- Classification metrics:
>> python main.py '2' 

- Given query classification:
>> python main.py '2' query(e.g. Partido Politico)

- Party statistics:
>> python main.py '3' filename('en_docs_clean.csv' or 'pt_docs_clean.csv')


In the ad-hoc.py file are defined all the functions needed to search the corpus. 

In the doc_retrieval.py are defined all the functions needed to process the dataset.
  
In the classification.py file are defined the functions that classify a query and the functions that measure the metrics, as well as some other ones that are used to process the data set into a panda dataframe.

In the stats.py file are the functions used to provide statistics on named entities in the corpus.

Finally, in the main.py is where we divide the 3 different functionalities.
