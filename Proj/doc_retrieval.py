import re
import string
from nltk.corpus import stopwords

def information2dic(filename):		#parses the file with the documents (done without panda library)

	lst = []

	# parse document
	with open(filename) as file: 
		first_line = file.readline()
		first_line = re.sub(r'[\n]', '', first_line) 
		first_line  = first_line.split(',')


		while True:
			flag = False
			text = ''
			line = file.readline()
			line = re.sub(r'[\n]', '', line)
			line_split = line.split(',')

			if line_split == ['']:
				break


			# parse titles with commas

			if line_split[-1][-1] == '"':
				count = -2
				st = line_split[-1]

				while(line_split[count][0] != '"'):
					st = line_split[count] + ',' + st 
					count -= 1
				
				st = line_split[count] + ',' + st
				line_split = line_split[:count] 
				line_split = line_split + [st]
				


			# text is split, join and add previously removed commas 
			
			text = line_split[0]
			for i in range(1, len(line_split) -4):
				text = text + ',' + line_split[i]
			

			#remove punctuation from text and more
	
			text = transform_text(text)
			
			


			for j in lst:
				if get_manifesto_id(j) == line_split[-4]:
					set_text(j, get_text(j) + ' ' + text)
					flag = True
					break



			if flag == False:		
				lst = lst + [{first_line[-1] : line_split[-1],
					first_line[-2] : line_split[-2],
					first_line[-3] : line_split[-3],
					first_line[-4] : line_split[-4],
					first_line[-5] : text}]


	file.close()					
	
	return lst


def set_text(el, text):
	el['text'] = text


def get_party(el):
	return(el['party']) 		

def get_text(el):
	return(el['text']) 

def get_manifesto_id(el):
	return(el['manifesto_id'])

def get_date(el):
	return(el['date'])

def get_title(el):
	return(el['title'])	

def transform_text(text):	#gets rid of stopwords, punctuation and upper case letters

	st = ''

	stopWords = set(stopwords.words('portuguese'))
	#print(stopWords)
	text = re.sub(r'[^\w\s-]','',text)
	#print(text)
	text.translate(string.punctuation)
	text = text.lower()

	text = text.split()
	#print(text)

	new_text = [word for word in text if word not in stopWords]

	for i in new_text:
		st = st + i + ' '

	return st




