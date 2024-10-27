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

app = Flask(__name__) # create an empty web app

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def analyze_sentiment(user_input):
  analysis = TextBlob(user_input)
  sentiment = analysis.sentiment.polarity
  return sentiment

def chatbot():
  print("Hello! I'm a chatbot.")
  print("How you feel about this game?") # Game A
  while True:
    user_input = input("User: ")
    sentiment = analyze_sentiment(user_input)

    data = {"user_answer":user_input, "sentiment":sentiment}
    db.child("chatbot").push(data)

    print(sentiment)
# Firebase Database
# Feedback
# - answer of the user
# - sentiment
# - index
@app.route('/dashboard')
def dashboard():
    feedbacks = db.child("feedbacks").get().val().values()
    sentiments = [feedback["sentiment"] for feedback in feedbacks] # ["Positive","Negative","Positive"...]
    sentiments_counts = Counter(sentiments) # {"Positive": 50, "Negative": 20, "Neutral" :10}
    sentiments_labels = list(sentiments_counts.keys()) # ["Positive", "Negative", "Neutral"]
    sentiments_data = list(sentiments_counts.values()) # [50, 20, 10]

    return render_template('dashboard.html',sentiments_labels=sentiments_labels,sentiments_data=sentiments_labels )

if __name__ == "__main__":
    app.run(debug=True) # running web-app