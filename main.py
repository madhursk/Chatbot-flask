from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask_sqlalchemy import SQLAlchemy
from flask import request
import os
import nltk
import random
import sqlite3
import nltk
import random
import pandas as pd


app = Flask(__name__)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.debug = True
db = SQLAlchemy(app)


# class Domain_Ext(db.Model):
# 	id = db.Column(db.Integer, primary_key= True)
# 	#uid = db.Column(db.String(100))
# 	question = db.Column(db.String(100))
# 	response = db.Column(db.String(100))
# 	kw = db.Column(db.String(100))

# 	def __init__(self, question, response, kw):
# 		#self.uid = uid
# 		self.question = question
# 		self.response = response
# 		self.kw = kw


# 	def __repr__(self):
# 		return f"Domain_Ext('{self.question}', '{self.response}', '{self.kw}')"



# class domain_selection(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	kw = db.Column(db.String(100))
# 	subdomain = db.Column(db.String(100))

# 	def __repr__(self):
# 		return f"domain_selection('{self.kw}', '{self.subdomain}')"





ask_phrases = ['Tell me something more about ','Can you elaborate about your work in ', 'This seems interesting... can you tell me more about ', 'What did you do in ']






@app.route('/')
def index():
	return render_template('index.html')


@app.route('/subdomain', methods=["GET", "POST"])
def subdomain():
	return render_template('subdomain.html')




@ app.route('/process', methods=['POST'])

# con = sqlite3.connect('chatbot.db')
# 			cursorObj = con.cursor()
# 			cursorObj.execute("INSERT INTO domain_ext (question, answer, keyword) VALUES (?,?,?)",(qtns[0],ans,nouns[0]))
# 			con.commit()
# 			cursorObj.close()

# return render_template('index.html',user_input=ans,bot_response=qtn)			
# 			ans = request.form['user_input']
# 			answers.append(ans)
# 			n_count=n_count+1

def process():
	# return render_template('index.html',bot_response="Tell me about your recent project")
	dict3 = ['paper', 'project', 'data', 'nothing', 'no', 'I', 'major', 'analysis', 'use', 'learning']
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()

	ans = request.form['user_input']
	uid = request.form['uid']

	
	qtns1 = "Tell me about your recent project"
	

	ask_phrases = ['Tell me something more about ',
               'Can you elaborate about your work in ', 
               'This seems interesting... can you tell me more about ', 
               'What did you do in ']


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
	cursorObj.execute("INSERT INTO domain_extraction (question, answer, keyword, user_id) VALUES (?,?,?,?)",(qtns1,ans,kw, uid))
	con.commit()
	cursorObj.close()

	names=[]
	imp_keywords = []
	con = sqlite3.connect('chatbot.db')
	cursorObj = con.cursor()
	cursorObj.execute("SELECT keyword from domain_extraction where user_id=\""+uid+"\"")
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
	cursorObj.execute("SELECT COUNT(uid) FROM domain_extraction where user_id=\""+uid+"\"")
	key_count = cursorObj.fetchall()
	print("keycountzzz")
	value_count = int(key_count[0][0])
	print(value_count)
	print(key_count)
	cursorObj.close()
	qtn = ''
	qtn = qtn + ask_phrases[random.randint(0,len(ask_phrases)-1)]
	qtn = qtn + final_imp_keywords[value_count-1] 


	return render_template('index.html',user_input=ans,bot_response=qtn,uid=uid)

	





		
	

	# user_input=request.form['user_input']

	# bot_response=bot.get_response(user_input)
	# bot_response=str(bot_response)
	# print("Friend: "+bot_response)
	# return render_template('index.html',user_input=user_input,
	# 	bot_response=bot_response
	# 	)


if __name__=='__main__':
	app.run(debug=True,port=5000)