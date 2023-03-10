import os
from flask import Flask, request, render_template
import pickle
from clean_text import TextProcess

app = Flask(__name__)

MODEL = pickle.load(open(os.path.normpath('models/model.pkl'), 'rb'))
WORD_VECTORIZER = pickle.load(open(os.path.normpath ("models/word_vectorizer.pkl"), 'rb'))
CLEAN_OBJ = TextProcess()

MAPPING = {'0': 'Negative', '1': 'Positive'}

def get_sentiment(text):
  vec = WORD_VECTORIZER.transform([text])
  pred = MODEL.predict(vec)
  return pred[0]

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # text = request.json['text']
        text = request.form['text'].lower()
        text1 = CLEAN_OBJ.clean_text(text)
        score = get_sentiment(text1)
        sentiment = MAPPING[str(score)]
        return render_template('form.html', final=True, text=text, sentiment=sentiment)
    else:
        return render_template('form.html')

if __name__=="__main__":
    app.run(debug=True)
