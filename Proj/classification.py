import numpy as np
from sklearn.model_selection import train_test_split
from doc_retrieval import *
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import Perceptron
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier



def create_dataset(csv):

	df = pd.read_csv(csv, names=["text","manifesto_id","party","date","title"])

	df = df.drop(df.index[0])	

	return df 

#----------------------------------------------------------------
#GETTERS

def get_text(df,row_number):
	
	text = df.loc[row_number]["text"]
	return text  	

def get_manifesto_id(df,row_number):

	manifesto_id = df.loc[row_number]["manifesto_id"]
	return manifesto_id

def get_party(df,row_number):

	party = df.loc[row_number]["party"]
	return party

def get_date(df,row_number):	

	date = df.loc[row_number]["date"]
	return date

def get_title(df, row_number):

	title = df.loc[row_number]["title"]
	return title	
	


def get_train_test(df, test_sz):

			
	X_train, X_test, y_train, y_test = train_test_split(df, df["party"].tolist()  ,  test_size = test_sz)
	return X_train, X_test, y_train, y_test 

#--------------------------------------------------------------------------------------------------------------------#
	
def choose_labels(X_train, X_test, y_train, y_test, classifier):
	

	#metrics of the classifiers

	stopWords = stopwords.words('portuguese')
	
	if classifier == 'nb':
		
		cls = MultinomialNB()
	
	elif classifier == 'knn':
	
		cls = KNeighborsClassifier()
	
	elif classifier == 'lm':
	
		cls = Perceptron()
	
	elif classifier == 'nn':
	
		cls = MLPClassifier(hidden_layer_sizes=(10,), max_iter=10)
	
	elif classifier == 'svm':
	
		cls = LinearSVC()

	

	v = TfidfVectorizer(stop_words= stopWords, ngram_range= (1,3))

	x = v.fit_transform(X_train["text"]) # transforming the words into values
		
	cls.fit(x, y_train)

	y = v.transform(X_test["text"]) # transforming the words into values

	y_pred = cls.predict(y)


	print(classifier + ":")

	
	print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

	print(metrics.classification_report(y_test, y_pred))


	 


def classify_query(X_train, y_train, query, classifier):

	#classifying the query

	stopWords = stopwords.words('portuguese')
	
	if classifier == 'nb':
		
		cls = MultinomialNB()
	
	elif classifier == 'knn':
	
		cls = KNeighborsClassifier()
	
	elif classifier == 'lm':
	
		cls = Perceptron()
	
	#elif classifier == 'nn':
	#
	#	cls = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(10,), max_iter=10)
	
	elif classifier == 'svm':
	
		cls = LinearSVC()
		
	else:
		print("ERROR: available classifiers are 'nb', 'knn', 'lm', 'nn' and 'svm'")
		exit()

	v = TfidfVectorizer(stop_words= stopWords, ngram_range= (1,3))

	x = v.fit_transform(X_train["text"])
		
	cls.fit(x, y_train)

	y = v.transform([query])

	print(cls.predict(y))

	







