import flask
from flask_bootstrap import Bootstrap
import pickle
from keras.models import model_from_json
from bs4 import BeautifulSoup
import re
from nltk.tokenize import WordPunctTokenizer
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = flask.Flask(__name__)
Bootstrap(app)
app.config["DEBUG"] = True


'''
Load the model with below code
'''
###################################################################
json_file = open('./model/rnnmodel_02_5.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights('./model/rnnmodel_02_5.h5')
print("Loaded model from disk")
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

token = None
with open('./model/tokenizer.pickle', 'rb') as handle:
   token = pickle.load(handle)
###################################################################

'''
clean input text data with below code
'''
###################################################################
tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))
ans = ['True', 'Fake']

def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    
    letters_only = re.sub("[^a-zA-Z.?,]", " ", clean)
    lower_case = letters_only.lower()
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip().replace(" .",'.').replace(" ?",'?').replace(" ,",',') 
###################################################################


'''
web page code
'''
###################################################################
@app.route('/')
def home():
    return flask.render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    input_text = flask.request.form.get("input_text")
    
    if input_text == "":
        return flask.redirect(flask.url_for("home"))

    ##############################
    clean_text = tweet_cleaner(input_text)
    test_sequences = token.texts_to_sequences([clean_text])
    test_sequences_padded = pad_sequences(test_sequences, maxlen=200)
    prediction_bs = loaded_model.predict(test_sequences_padded)
    predictions=np.where(prediction_bs<0.5,0,1) 

    ##############################

    return flask.render_template("index.html", predict_result=ans[predictions[0][0]])

@app.route('/analysis')
def analysis():
    return "hello world"
###################################################################

if __name__ == "__main__":
    app.run(debug=True)