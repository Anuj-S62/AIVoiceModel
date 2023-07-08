import spacy

def preProcess(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    filtered_token = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        filtered_token.append(token.lemma_)
    
    return " ".join(filtered_token)

def getIntent(text):    
    with open('nlu_model', 'rb') as f:
        model = pickle.load(f)
    text = preProcess(text)
    return model.predict([text])[0]

def main():

    text = preProcess(text)
    prediction = getIntent(text)
    print(prediction)
    if prediction=='changeVolume':
        percentage = '10'
        doc = nlp(text)
        for token in doc:
            if token.is_digit:
                percentage = token
        return {'volume':str(percentage)},200

    if prediction=='openApp':
        apps = ['phone','contacts','settings','alarm','youtube','music player','musicplayer','photos','gallery','messages','clock','camera','calculator']
        doc = nlp(text)

        for token in doc:
            if str(token) in apps:
                return {'app':str(token)},200
    return {},404


