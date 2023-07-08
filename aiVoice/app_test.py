from flask import Flask,request
import spacy
import pickle

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello</p>"

with open('nlu_model_2', 'rb') as f:
        model = pickle.load(f)

nlp = spacy.load("en_core_web_sm")

def preProcess(text):
    
    doc = nlp(text)
    filtered_token = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        filtered_token.append(token.lemma_)
    
    return " ".join(filtered_token)

def getIntent(text):    
    
    text = preProcess(text)
    return model.predict([text])[0]

@app.route('/getIntent',methods=['POST'])
def finalModel("set an alarm for 5 p.m."):
    # text = request.form.get('text')
    text = text.lower()
    text = preProcess(text)
    prediction = getIntent(text)
    print(prediction)
    if prediction=='changeVolume':
        percentage = '10'
        doc = nlp(text)
        for token in doc:
            if token.is_digit:
                percentage = token
        return {"intentName":'volume','intentValue':str(percentage),"response":"empty"},200
    if prediction=='openApp':
        apps = ['phone','contacts','settings','alarm','youtube','music player','music','musicplayer','photos','gallery','messages','clock','camera','calculator']
        doc = nlp(text)

        for token in doc:
            if str(token) in apps:
                return {"intentName":'app','intentValue':str(token),"response":"empty"},200
    return {},404


print(getIntent())
# if __name__ == '__main__':
#     app.run(debug=True)