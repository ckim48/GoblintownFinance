# python library
# textblob  --> Calculting the sentiment score of the given text
# pyrebase  --> Using database which store the collected data from chatbot
# flask  --> Web application using python
# Main Goal: Create Web Dashboard which contains lots charts which helps the admin
#            to decide future finance strategy. + Chatbot

from flask import *
app = Flask(__name__) # create an empty web app

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True) # running web-app