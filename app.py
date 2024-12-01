# python library
# textblob  --> Calculting the sentiment score of the given text
# pyrebase  --> Using database which store the collected data from chatbot
# flask  --> Web application using python
# Main Goal: Create Web Dashboard which contains lots charts which helps the admin
#            to decide future finance strategy. + Chatbot
from flask import *
from textblob import TextBlob
from config import firebaseConfig
import pyrebase
from collections import Counter
import yake

app = Flask(__name__) # create an empty web app

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
def analyze_sentiment(user_input):
  analysis = TextBlob(user_input)
  sentiment = analysis.sentiment.polarity
  return sentiment
lst = ["How do you feel about this game?", "Have you purchased any in-game purchasing item?","How do you feel about the in-game purchases?", "Do you feel that the prices for in-game purchases are fair?", "What type of in-game purchases do you enjoy the most?", "What is your gender?", "What is your age?"]
def chatbot():
  extractor = yake.KeywordExtractor(lan="en", n=1, top=3) # we are going to extract the 3 most important words
  print("Hello! I'm a chatbot.")
  for i in range(len(lst)): # 0 ~ 2
    print(lst[i])
    user_input = input("User: ") # I love it
    keywords = extractor.extract_keywords(user_input)
    sentiment = analyze_sentiment(user_input) # 0.5
    data = {"question_number": i+1, "user_answer":user_input, "sentiment":sentiment, "keywords": keywords}
    db.child("chatbot").push(data) # Adding the data into our database
    print(sentiment)
# Firebase Database
# Feedback
# - answer of the user
# - sentiment
# - index
@app.route('/dashboard')
def dashboard():
    feedbacks = db.child("chatbot").get().val().values() # every data under document 'chatbot'
    sum_sentiment = 0
    count = 0
    for feedback in feedbacks:
        # print(feedback)
        if feedback["question_number"] != 2 and feedback["question_number"] != 6 and feedback["question_number"] != 7:
            sum_sentiment += feedback["sentiment"]
            count += 1
    average_sentiment = sum_sentiment/count
    print("Average Sentiment", average_sentiment)
    return render_template('dashboard.html', average_sentiment = average_sentiment)

if __name__ == "__main__":
    # chatbot()
    app.run(debug=True) # running web-app