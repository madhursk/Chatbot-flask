from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask_sqlalchemy import SQLAlchemy
import os
import nltk
import random
bot = ChatBot('Friend') #create the bot

#bot.set_trainer(ListTrainer) # Teacher
trainer = ListTrainer(bot)
#bot.train(conv) # teacher train the bot

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Domain_Ext(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	question = db.Column(db.String(100))
	answer = db.Column(db.String(100))
	Keywords = db.Column(db.String(100))

	def __repr__(self):
		return f"Domain_Ext('{self.id}', '{self.question}', '{self.answer}', '{self.Keywords}')"



class domain_selection(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	Keywords = db.Column(db.String(100))
	subdomain = db.Column(db.String(100))

	def __repr__(self):
		return f"domain_selection('{self.Keywords}', '{self.subdomain}')"





ask_phrases = ['Tell me something more about ','Can you elaborate about your work in ', 'This seems interesting... can you tell me more about ', 'What did you do in ']

flimit = 4

for knowledeg in os.listdir('base'):
	BotMemory = open('base/'+ knowledeg, 'r').readlines()
	trainer.train(BotMemory)







@app.route('/')
def index():
	return render_template('index.html')

@ app.route('/process', methods=['POST'])



# def nouns_extract(nouns,ans):
# 	# ask_phrases = ['Tell me something more about ','Can you elaborate about your work in ', 'This seems interesting... can you tell me more about ', 'What did you do in ']
# 	words = nltk.word_tokenize(ans)
# 	list_words = nltk.pos_tag(words)
# 	for i in range(len(list_words)):
# 		if("NN" in list_words[i][1]):
# 			if(i+1<len(list_words)):
# 				if("NN" in list_words[i+1][1]):
# 					nouns.append(list_words[i][0]+" "+list_words[i+1][0])
# 					print(list_words[i][0]+" "+list_words[i+1][0])
# 			else:
# 				nouns.append(list_words[i][0])
# 				print(list_words[i][0])
# 	return nouns

# flimit = 4
def process():
	answers = []
	count = 0
	ans = request.form['user_input']
	# ans=str(input('Tell me about the topics used in your recent project'))
	answers.append(ans)

	nouns = []
	n_count=0
	

	
	while(len(answers)<4):
		# nouns = nouns_extract(nouns,answers[count])
		
		words = nltk.word_tokenize(ans)
		list_words = nltk.pos_tag(words)
		for i in range(len(list_words)):
			if("NN" in list_words[i][1]):
				if(i+1<len(list_words)):
					if("NN" in list_words[i+1][1]):
						nouns.append(list_words[i][0]+" "+list_words[i+1][0])
						print(list_words[i][0]+" "+list_words[i+1][0])
					else:
						nouns.append(list_words[i][0])
				else:
					nouns.append(list_words[i][0])
					print(list_words[i][0])


		print(str(count) + " ---> ")
		print(nouns)
		count=count+1
		while(n_count<len(nouns)):
			
			qtn = ''
			qtn = qtn + ask_phrases[random.randint(0,len(ask_phrases)-1)]
			qtn = qtn + nouns[n_count] + '\n'
		#     print(qtn)
			
			return render_template('index.html',user_input=ans,bot_response=qtn)			
			ans = request.form['user_input']
			answers.append(ans)
			n_count=n_count+1

		
	

	# user_input=request.form['user_input']

	# bot_response=bot.get_response(user_input)
	# bot_response=str(bot_response)
	# print("Friend: "+bot_response)
	# return render_template('index.html',user_input=user_input,
	# 	bot_response=bot_response
	# 	)


if __name__=='__main__':
	app.run(debug=True,port=5000)