from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request
import os
import nltk
import random
import sqlite3
import nltk
import random
import pandas as pd
import requests
import string
import operator
from lxml import html
from googlesearch import search
from bs4 import BeautifulSoup
import re


app = Flask(__name__)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.debug = True
db = SQLAlchemy(app)

# unique_id = ''

ask_phrases = ['Tell me something more about ','Can you elaborate about your work in ', 'This seems interesting... can you tell me more about ', 'What did you do in ']

@app.route('/')
def index():
	return render_template('index.html')









# to generate links
@app.route('/link1',methods=['POST'])
def applications():
	applications = request.form['sub_apps_user']
	app_priority = request.form['app_priority_user']
	# print("----------------------Applications-------------------------------")
	print(applications)

	Dict1 = {'MachineLearning': ['StockPredictions','ProductRecommendations','WebSearchEngine','FraudDetection','Analytics'],
	'ArtificialIntelligence': ['AutomatedCustomerSupport', 'Healthcare', 'SmartCars','SmartHomeDevices', 'ArtificialGeneralIntelligence'],
	'DeepLearning': ['ImageRecognition','FraudDetection','SpeechRecognition','AnomalyDetection', 'FaceDetection'],
	'ComputerVision': ['FaceDetection', 'TerrainDetection','MotionAnalysis','ImageRestoration','ImageProcessing'],
	'DigitalImageProcessing': ['ImageRestoration','PatternRecognition','PatternRecognition','LinearFiltering','RemoteSensing'],
	'CloudComputing': ['BigDataAnalytics', 'StoringPurpose','ProcessingPurpose','TestAndDevelopment','E-CommerceSoftware'],
	'BigData': ['StoragePurpose','ProcessingPurpose', 'WeatherForecasting', 'TrafficOptimization', 'AnalyticsProcessing'],
	'DataAnalytics': ['AnalyticsProcessing','DataProcessing','DataVisualtization', 'EnergyManagement', 'Gaming'],
	'InternetOfThings': ['Automations','SmartHomes','SmartWearables', 'ConnectedCars', 'SmartCities'],
	'ComputerNetworks': ['TransferProtocol','CommunicationsMedium','FileTransfer','TrafficControl', 'HybridComputing'],
	'DataBaseManagementSystem' : ['ECommerceManagementSystem', 'StoreManagementSystem','StorageManagement','RecoveryManagement','SecurityManagement'],
	'Blockchain' : ['SmartAppliances','CryptoCurrency','FraudDetection','Tokenization','PersonalIdentification'],
	}


	print("========================Printing applications")


	print(applications)


	list_x = applications.split(";")[:-1]
	list_y = app_priority.split(";")[:-1]

	dict_domains_nfinal = []
	dict_domains_pr_nfinal = []
	for substrings in list_x:
		dict_domains_nfinal.append(substrings.split(",")[:-1])

	for substrings in list_y:
		dict_domains_pr_nfinal.append(substrings.split(",")[:-1])

	print(dict_domains_nfinal)
	print(dict_domains_pr_nfinal)

	for i in range(1,len(dict_domains_nfinal)):
		semi_list = dict_domains_nfinal[i]
		semi_list = semi_list[1:]
		dict_domains_nfinal[i]=semi_list
	print(dict_domains_nfinal)

	for i in range(1,len(dict_domains_pr_nfinal)):
		semi_list = dict_domains_pr_nfinal[i]
		semi_list = semi_list[1:]
		dict_domains_pr_nfinal[i]=semi_list
	print(dict_domains_pr_nfinal)

	# array form of user choice
	final_dict = {}
	for i in dict_domains_nfinal:
		list_z = []
		for z in range(1,len(i)):
			list_z.append(int(i[z]))
		final_dict[i[0]] = list_z
	print(final_dict)

	final_pr_dict = {}
	for i in dict_domains_pr_nfinal:
		list_z = []
		for z in range(1,len(i)):
			list_z.append(int(i[z]))
		final_pr_dict[i[0]] = list_z
	print(final_pr_dict)


	super_final_array = []
	for i in final_dict:
		x = Dict1[i]
		super_final_array.append([i,5])
		for y in range(len(x)):
			if(final_dict[i][y] == 1):
				super_final_array.append([x[y],final_pr_dict[i][y]])
	print(super_final_array)

	for i in super_final_array:
			con = sqlite3.connect('chatbot.db')
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO keywords (keyword,priority) VALUES (\""+i[0]+"\",\""+str(i[1])+"\")")
			con.commit()
			cursorObj.close()


	# Now the applications are inserted into the table
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	cursorObj.execute("SELECT keyword,priority FROM keywords")
	con.commit()
	#cursorObj.close()

	rows1 = cursorObj.fetchall()
	cursorObj.close()
	print("printing rowss--------------------------------------------")
	nsuperfinal_keywords = []
	for row in rows1:
	    # print(row)
		nsuperfinal_keywords.append([row[0],int(row[1])])
	print(nsuperfinal_keywords)


	# taking the keywords from the initial list as well
	names=[]
	imp_keywords = []
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	cursorObj.execute("SELECT keyword from domain_extraction")
	rows1 = cursorObj.fetchall()
	cursorObj.close()
	print("printing rowss")
	for row in rows1:
		print(row)
		names.append(row[0])


	for i in range(len(names)):
		imp_keywords = imp_keywords + str(names[i]).split('; ')


	print("printing imp keywords")
	print(imp_keywords)


	dict4 = ['','nan']
	final_imp_keywords = []
	for i in imp_keywords:
		if(i not in dict4):
			final_imp_keywords.append(i)
			nsuperfinal_keywords.append([i,10])

	print("printing final keywords")
	print(final_imp_keywords)

	extra = []
	superfinal_keywords = []
	for i in nsuperfinal_keywords:
		if(str(re.sub("([a-z])([A-Z])","\g<1> \g<2>",i[0])).lower() not in extra):
			superfinal_keywords.append([re.sub("([a-z])([A-Z])","\g<1> \g<2>",i[0]).lower(),i[1]])
			extra.append(re.sub("([a-z])([A-Z])","\g<1> \g<2>",i[0]).lower())

	print(superfinal_keywords)
	print("printing extra  : \n"+str(extra)+"\n\n")

	keywords = superfinal_keywords
	q1 = ''
	for i in keywords:
	    q1 = q1 + ' + ' + i[0]
	# print(q1)
	query = q1[3:]

	# query = "IEEE xplore + ieee " + query
	print(query)
	fallback = 'Sorry, The title didnt exist for this page.'
	result = ''
	titles = []
	page_content=[]
	# index = 0
	search_result_list = list(search(query, tld="co.in", num=7, stop=7, pause=1))
	print(search_result_list)

	for index in range(0,7):
		result=''
		flag=0
		try:
		#         print(1)
		    page = requests.get(search_result_list[index])
		    print(search_result_list[index])
		#     print(page)
		    tree = html.fromstring(page.content)

		    soup = BeautifulSoup(page.content, features="lxml")
		#     print(soup)
		    article_text = ''
		    page_content.append(soup)
		    article = soup.findAll('title')
		    for element in article:
		        article_text += '\n' + ''.join(element.findAll(text = True))
		    article_text = article_text.replace('\n', '')
		    first_sentence = article_text.split('.')
		    first_sentence = first_sentence[0].split('?')[0]
		#         first_sentence = article
		    print(first_sentence)
		    chars_without_whitespace = first_sentence.translate(
		        { ord(c): None for c in string.whitespace }
		    )

		    if len(chars_without_whitespace) > 0:
		        result = first_sentence
		    if(str(result)!="403 Forbidden"):
		        titles.append(result)
		    else:
		        result = fallback
			#if (str(result) != "403 Forbidden"):
			# 	titles.append(result)
		except:
			flag=1
		     #if (len(result) == 0):
		       # result = fallback
		    # print(result)

		     #print(titles)
			# continue
		#if flag == 1:
			#continue
		#titles.append(result)
	print("printing titles==========================>>>>>>>>>>>>>>>>>>>>>=================")
	print(titles)
	print("\n\n\n")
	weights = []
	priority = []
	for i in superfinal_keywords:
	    priority.append(i[1])
		#priority.append(1)
	for i in page_content:
	    list1 = []
	    for j in range(0,len(superfinal_keywords)):
	        count_word = str(i).count(str(superfinal_keywords[j][0]))
	        list1.append(count_word*superfinal_keywords[j][1])
	    weights.append(list1)
	print(weights)

	score = {}
	links = {}
	counter = 0
	for i in titles:
		if(i != ''):
		    score[i]=sum(weights[counter])
		    links[i]=search_result_list[counter]
		else:
		    score[str(counter)]=sum(weights[counter])
		    links[str(counter)]=search_result_list[counter]
		counter= counter+1

	sorted_d = sorted(score.items(), key=operator.itemgetter(1))
	sorted_d.reverse()
	print(sorted_d)

	sending_links = ""
	for key,value in sorted_d:
		print(links[key])
		sending_links = sending_links + links[key] + "¬" + key + ";"

	# Clearing the database
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	cursorObj.execute("DELETE FROM domain_extraction")
	con.commit()
	#cursorObj.close()
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	cursorObj.execute("DELETE FROM keywords")
	con.commit()
	cursorObj.close()





	return render_template('final_op.html',links = sending_links)












# domains getting from user and sending applications
@app.route('/application1', methods=['POST','GET'])
def subdomain():
	Dict = {'MachineLearning': ['LinearRegression','LogisticRegression','KNN','SupervisedLearning','UnSupervisedLearning','NaiveBayes'],
	'ArtificialIntelligence': ['KnowledgeReasoning', 'Planning', 'NaturalLanguageProcessing', 'ComputerVision', 'Robotics', 'ArtificialGeneralIntelligence'],
	'DeepLearning': ['ImageRecognition','FraudDetection','RecommendationSystem','SupervisedLearning','NeuralNetworks','AnomalyDetection'],
	'ComputerVision': ['Recognition','MotionAnalysis','ImageRestoration','ImageProcessing'],
	'DigitalImageProcessing': ['ImageRestoration','Classification','PatternRecognition','LinearFiltering','Projection'],
	'CloudComputing': ['InfrastructureAsAService','PlatformAsAService','SoftwareAsAService','FunctionAsAService','DistributedCloud','BigData'],
	'BigData': ['Hadoop','Hive','Pig','Spark','CloudComputing','MapAndReduce'],
	'DataAnalytics': ['Hadoop','MapAndReduce','DataCleaning','DataProcessing','DataCollection','DataVisualtization'],
	'InternetOfThings': ['RasberryPi','Microprocessor','Microcontroller'],
	'ComputerNetworks': ['TCP','UDP','IP'],
	'DataBaseManagementSystem' : ['DataBase','ManagementSystem','StructuredQueryLanguage','Transactions','QueryControl'],
	'Blockchain' : ['Crytography','Public','Private','Ledger','Contracts'],
	}

	# Values selected by user as subdomains in string form
	subdomains_user = request.form['sub_domains_user']
	print("========================Printing subdomians")
	print(subdomains_user)
	subpriority_user = request.form['sub_priority_user']
	print("========================Printing subpriorities")
	print(subpriority_user)


	list_x = subdomains_user.split(";")[:-1]
	list_y = subpriority_user.split(";")[:-1]

	dict_domains_nfinal = []
	dict_domains_pr_nfinal = []
	for substrings in list_x:
		dict_domains_nfinal.append(substrings.split(",")[:-1])

	for substrings in list_y:
		dict_domains_pr_nfinal.append(substrings.split(",")[:-1])

	print(dict_domains_nfinal)
	print(dict_domains_pr_nfinal)

	for i in range(1,len(dict_domains_nfinal)):
		semi_list = dict_domains_nfinal[i]
		semi_list = semi_list[1:]
		dict_domains_nfinal[i]=semi_list
	print(dict_domains_nfinal)

	for i in range(1,len(dict_domains_pr_nfinal)):
		semi_list = dict_domains_pr_nfinal[i]
		semi_list = semi_list[1:]
		dict_domains_pr_nfinal[i]=semi_list
	print(dict_domains_pr_nfinal)

	# array form of user choice
	final_dict = {}
	for i in dict_domains_nfinal:
		list_z = []
		for z in range(1,len(i)):
			list_z.append(int(i[z]))
		final_dict[i[0]] = list_z
	print(final_dict)

	final_pr_dict = {}
	for i in dict_domains_pr_nfinal:
		list_z = []
		for z in range(1,len(i)):
			list_z.append(int(i[z]))
		final_pr_dict[i[0]] = list_z
	print(final_pr_dict)


	super_final_array = []
	for i in final_dict:
		x = Dict[i]
		super_final_array.append([i,5])
		for y in range(len(x)):
			if(final_dict[i][y] == 1):
				super_final_array.append([x[y],final_pr_dict[i][y]])
	print(super_final_array)

	for i in super_final_array:
			con = sqlite3.connect('chatbot.db')
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO keywords (keyword,priority) VALUES (\""+i[0]+"\",\""+str(i[1])+"\")")
			con.commit()
			cursorObj.close()


	# Now the keywords are inserted into the table and
	# we are forming and applications dictionary to send to applications.html

	# Dictionary for applications addition to the chatbot
	# Dict1 = {'MachineLearning': ['Predictions','Recommenadations','WebSearchEngine','Detection','Analytics'],
	# 'ArtificialIntelligence': ['Recognition', 'Detection', 'Recomendation','Prediction', 'ArtificialGeneralIntelligence','Analytics'],
	# 'DeepLearning': ['ImageRecognition','FraudDetection','RecommendationSystem','AnomalyDetection'],
	# 'ComputerVision': ['Recognition','MotionAnalysis','ImageRestoration','ImageProcessing'],
	# 'DigitalImageProcessing': ['ImageRestoration','Classification','PatternRecognition','LinearFiltering','Projection'],
	# 'CloudComputing': ['Applications', 'Storing','Processing'],
	# 'BigData': ['Storage','Processing'],
	# 'DataAnalytics': ['Analytics','Processing','Visualtization'],
	# 'InternetOfThings': ['Automations','SmartHomes','Wearables'],
	# 'ComputerNetworks': ['TransferProtocol','Communications'],
	# 'DataBaseManagementSystem' : ['ManagementSystem','StorageManagement','RecoveryManagement','SecurityManagement'],
	# 'Blockchain' : ['Crytography','CryptoCurrency','Security','Tokenization'],
	# }
	Dict1 = {'MachineLearning': ['StockPredictions','ProductRecommendations','WebSearchEngine','FraudDetection','Analytics'],
	'ArtificialIntelligence': ['AutomatedCustomerSupport', 'Healthcare', 'SmartCars','SmartHomeDevices', 'ArtificialGeneralIntelligence'],
	'DeepLearning': ['ImageRecognition','FraudDetection','SpeechRecognition','AnomalyDetection', 'FaceDetection'],
	'ComputerVision': ['FaceDetection', 'TerrainDetection','MotionAnalysis','ImageRestoration','ImageProcessing'],
	'DigitalImageProcessing': ['ImageRestoration','PatternRecognition','PatternRecognition','LinearFiltering','RemoteSensing'],
	'CloudComputing': ['BigDataAnalytics', 'StoringPurpose','ProcessingPurpose','TestAndDevelopment','E-CommerceSoftware'],
	'BigData': ['StoragePurpose','ProcessingPurpose', 'WeatherForecasting', 'TrafficOptimization', 'AnalyticsProcessing'],
	'DataAnalytics': ['AnalyticsProcessing','DataProcessing','DataVisualtization', 'EnergyManagement', 'Gaming'],
	'InternetOfThings': ['Automations','SmartHomes','SmartWearables', 'ConnectedCars', 'SmartCities'],
	'ComputerNetworks': ['TransferProtocol','CommunicationsMedium','FileTransfer','TrafficControl', 'HybridComputing'],
	'DataBaseManagementSystem' : ['ECommerceManagementSystem', 'StoreManagementSystem','StorageManagement','RecoveryManagement','SecurityManagement'],
	'Blockchain' : ['SmartAppliances','CryptoCurrency','FraudDetection','Tokenization','PersonalIdentification'],
	}


	names=[]
	imp_keywords = []
	# uid = request.form['uid']
	# uid = unique_id
	# print(str(uid)+"\n\n")
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	# cursorObj.execute("SELECT keyword from domain_extraction where user_id=\""+uid+"\"")
	cursorObj.execute("SELECT keyword from domain_extraction")
	rows1 = cursorObj.fetchall()
	cursorObj.close()
	print("printing rowss--------------------------------------------")
	for row in rows1:
	    print(row)
	    names.append(row[0])
	for i in range(len(names)):
	    imp_keywords = imp_keywords + str(names[i]).split('; ')

	print("printing imp keywords--------------------------------------------")
	print(imp_keywords)

	dict4 = ['','nan']

	final_imp_keywords = []
	for i in imp_keywords:
	    if(i not in dict4):
	        final_imp_keywords.append(i)
	print("printing final keywords-----------------------------------------")
	print(final_imp_keywords)

	nouns = []
	for i in final_imp_keywords:
	    if(i not in nouns):
	        nouns.append(i)

	# nouns = final_imp_keywords
	imp_words = []
	indexes = []
	for word in nouns:
	    imp_words.append(word.replace(" ", ""))


	for i in range(len(imp_words)):
	    for j in Dict:
	        if(imp_words[i].lower() in j.lower() or check_in_dict(imp_words[i],Dict[j])):
	            indexes.append([imp_words[i],j])
	# finding the domains user is interested and taking their subdomains

	user_subdomains = {}
	for i in indexes:
	    user_subdomains[i[1]] = Dict1[i[1]]
	print("printing user subdomins ------------------------------- before sending")
	print(user_subdomains)

	# return render_template('subdomain.html',user_domains= user_subdomains)

	# user_subdomians_1 = request.form['sub_domains_user']
	# print("printing user subdomains ----------------------------------------")
	# print(user_subdomians_1)
	final_sending_list = ""
	for i in user_subdomains:
		final_sending_list = final_sending_list + i + ","
		for j in user_subdomains[i]:
			# list_x.append(j)
			final_sending_list = final_sending_list + j + ","
		final_sending_list = final_sending_list[:-1] + ";"




	return render_template('applicat.html',applications_list = final_sending_list)





def check_in_dict(value, listx):
	# ret_val = False
	for i in listx:
		if(value.lower() == i.lower()):
			return True
	return False





# Domains extraction from user
@app.route('/subdomain1', methods=['POST','GET'])
def subdomain1():

	# if request.method == 'POST':
	Dict = {'MachineLearning': ['LinearRegression','LogisticRegression','KNN','SupervisedLearning','UnSupervisedLearning','NaiveBayes'],
	'ArtificialIntelligence': ['KnowledgeReasoning', 'Planning','NaturalLanguageProcessing', 'ComputerVision', 'Robotics', 'ArtificialGeneralIntelligence'],
	'DeepLearning': ['ImageRecognition','FraudDetection','RecommendationSystem','SupervisedLearning','NeuralNetworks','AnomalyDetection'],
	'ComputerVision': ['Recognition','MotionAnalysis','ImageRestoration','ImageProcessing'],
	'DigitalImageProcessing': ['ImageRestoration','Classification','PatternRecognition','LinearFiltering','Projection'],
	'CloudComputing': ['InfrastructureAsAService','PlatformAsAService','SoftwareAsAService','FunctionAsAService','DistributedCloud','BigData'],
	'BigData': ['Hadoop','Hive','Pig','Spark','CloudComputing','MapAndReduce'],
	'DataAnalytics': ['Hadoop','MapAndReduce','DataCleaning','DataProcessing','DataCollection','DataVisualtization'],
	'InternetOfThings': ['RasberryPi','Microprocessor','Microcontroller'],
	'ComputerNetworks': ['TCP','UDP','IP'],
	'DataBaseManagementSystem' : ['DataBase','ManagementSystem','StructuredQueryLanguage','Transactions','QueryControl'],
	'Blockchain' : ['Crytography','Public','Private','Ledger','Contracts'],
	}

	# return render_template('subdomain.html')

	names=[]
	imp_keywords = []
	# uid = request.form['uid']
	# uid = unique_id
	# print(str(uid)+"\n\n")
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	# cursorObj.execute("SELECT keyword from domain_extraction where user_id=\""+uid+"\"")
	cursorObj.execute("SELECT keyword from domain_extraction")
	rows1 = cursorObj.fetchall()
	cursorObj.close()
	print("printing rowss--------------------------------------------")
	for row in rows1:
	    print(row)
	    names.append(row[0])
	for i in range(len(names)):
	    imp_keywords = imp_keywords + str(names[i]).split('; ')

	print("printing imp keywords--------------------------------------------")
	print(imp_keywords)

	dict4 = ['','nan']

	final_imp_keywords = []
	for i in imp_keywords:
	    if(i not in dict4):
	        final_imp_keywords.append(i)
	print("printing final keywords-----------------------------------------")
	print(final_imp_keywords)

	nouns = []
	for i in final_imp_keywords:
	    if(i not in nouns):
	        nouns.append(i)

	# nouns = final_imp_keywords
	imp_words = []
	indexes = []
	for word in nouns:
	    imp_words.append(word.replace(" ", ""))


	for i in range(len(imp_words)):
	    for j in Dict:
	        if(imp_words[i].lower() in j.lower() or check_in_dict(imp_words[i],Dict[j])):
	            indexes.append([imp_words[i],j])
	# finding the domains user is interested and taking their subdomains

	user_subdomains = {}
	for i in indexes:
	    user_subdomains[i[1]] = Dict[i[1]]
	print("printing user subdomins ------------------------------- before sending")
	print(user_subdomains)

	# return render_template('subdomain.html',user_domains= user_subdomains)

	# user_subdomians_1 = request.form['sub_domains_user']
	# print("printing user subdomains ----------------------------------------")
	# print(user_subdomians_1)
	final_sending_list = ""
	for i in user_subdomains:
		final_sending_list = final_sending_list + i + ","
		for j in user_subdomains[i]:
			# list_x.append(j)
			final_sending_list = final_sending_list + j + ","
		final_sending_list = final_sending_list[:-1] + ";"
		# final_sending_list.append(list_x)
	return render_template('subdomain.html',user_domains= final_sending_list)



@ app.route('/process', methods=['POST'])


def process():
	# return render_template('index.html',bot_response="Tell me about your recent project")
	dict3 = ['paper', 'project', 'data', 'nothing', 'no', 'I', 'major', 'analysis', 'use', 'learning', 'topic', 'topics', 'i', 'used']
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()

	ans = request.form['user_input']
	# uid = request.form['uid']
	# unique_id=uid

	qtns1 = "Tell me what do you want to do in your recent project"


	ask_phrases = ['Tell me something more about ',
               'Can you elaborate about your work in ',
               'This seems interesting... can you tell me more about ',
               'What did you do in ',
			   'What more topics did you do besides ',
			   'Any other topics you used in your project besides ',
			   'What other topics excite you apart from ',
			   'What applications are you interested in related to topic ']


	count = 0
	kw = []

	nouns = []
	n_count=0
	words = nltk.word_tokenize(ans)
	list_words = nltk.pos_tag(words)
	for i in range(len(list_words)):
		if("NN" in list_words[i][1]):
			if(i+1<len(list_words)):
				if("NN" in list_words[i+1][1]):
					nouns.append(list_words[i][0]+" "+list_words[i+1][0])
					print(list_words[i][0]+" "+list_words[i+1][0])
				else:
					if(list_words[i][0] not in dict3):
						nouns.append(list_words[i][0])
			else:
				if(list_words[i][0] not in dict3):
					nouns.append(list_words[i][0])
				print(list_words[i][0])
	print(str(count) + " ---> ")
	print(nouns)
	kw = ""
	for i in nouns:
		kw = kw + i + "; "

	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	cursorObj.execute("INSERT INTO domain_extraction (question, answer, keyword) VALUES (?,?,?)",(qtns1,ans,kw))
	con.commit()
	cursorObj.close()

	names=[]
	imp_keywords = []
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	cursorObj.execute("SELECT keyword from domain_extraction")
	rows1 = cursorObj.fetchall()
	cursorObj.close()
	print("printing rowss")
	for row in rows1:
		print(row)
		names.append(row[0])


	for i in range(len(names)):
		imp_keywords = imp_keywords + str(names[i]).split('; ')


	print("printing imp keywords")
	print(imp_keywords)


	dict4 = ['','nan']
	final_imp_keywords = []
	for i in imp_keywords:
		if(i not in dict4):
			final_imp_keywords.append(i)

	print("printing final keywords")
	print(final_imp_keywords)
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	cursorObj.execute("SELECT COUNT(question) FROM domain_extraction")
	key_count = cursorObj.fetchall()
	print("keycountzzz")
	value_count = int(key_count[0][0])
	print(value_count)
	print(key_count)
	cursorObj.close()
	qtn = ''
	qtn = qtn + ask_phrases[random.randint(0,len(ask_phrases)-1)]
	if((value_count)<=len(final_imp_keywords)):
		qtn = qtn + final_imp_keywords[value_count-1]
	else:
		qtn='Tell me more details about your project'


	return render_template('index.html',user_input=ans,bot_response=qtn)










	# user_input=request.form['user_input']

	# bot_response=bot.get_response(user_input)
	# bot_response=str(bot_response)
	# print("Friend: "+bot_response)
	# return render_template('index.html',user_input=user_input,
	# 	bot_response=bot_response
	# 	)


if __name__=='__main__':
	app.run(debug=True,port=5000)
