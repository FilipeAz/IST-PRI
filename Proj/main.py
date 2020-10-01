import sys
import fileinput
from ad_hoc import calculate_BM25, calculate_stats, show_status
from doc_retrieval import *
from classification import *
from stats import *




if __name__ == '__main__':

	if len(sys.argv)<2:
		print("ERROR: No option was given")

	elif sys.argv[1] == "1":
		


		if len(sys.argv)<3:
			print("ERROR: No query was given")
			exit
		
		lst = information2dic("pri_project_data/pt_docs_clean.csv")		#parse the file and join the same manifestos
		
		results, new_keywords = calculate_BM25(sys.argv[2:], lst)	#results are the manifestos with best scores and new_keywords is the query without stopwords (only used for statistics)
		lst_keywords = calculate_stats(lst, new_keywords)	#calculate statistics

		show_status(results, sys.argv[2:], lst, lst_keywords) #print statistics
		
		
	elif sys.argv[1] == "2":
		dataset = create_dataset("pri_project_data/pt_docs_clean.csv")	#parse the file and save in a panda frame (manifestos separated)
		
		if len(sys.argv) > 2:
			
			X_train, X_test, y_train, y_test = get_train_test(dataset, 0)	#when a query is given we use all the dataset as training
			
			query = ""
			
			for i in range(2, len(sys.argv)):
				
				query += " " +  sys.argv[i]		#joining the query in a string since it comes in a list
				
			classify_query(X_train, y_train, query, 'svm')	#classify the query (svm because meh)
			
		else:
		
			X_train, X_test, y_train, y_test = get_train_test(dataset, 0.2)		#when no query is given we test with 5 different classifiers to test accuracy, precision, recall, f1 and support

			choose_labels(X_train, X_test, y_train, y_test, 'nb')		#naive bayes
			choose_labels(X_train, X_test, y_train, y_test, 'knn')		#k nearest neighbors
			choose_labels(X_train, X_test, y_train, y_test, 'lm')		#linear model
			#choose_labels(X_train, X_test, y_train, y_test, 'nn')		#neural networks
			choose_labels(X_train, X_test, y_train, y_test, 'svm')		#support vector machines
		
	elif sys.argv[1] == "3":
	
		if len(sys.argv)<3:
			print("ERROR: No filename was given")
			exit
			
		getstats(sys.argv[2])		#just print the different statistics requested
		
		
		
		