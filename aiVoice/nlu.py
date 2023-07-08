# import pandas as pd
import spacy
# import re
# import json
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.feature_extraction.text import TfidfVectorizer


# f = open('intents.json')
  
# data = json.load(f)

nlp = spacy.load("en_core_web_sm")


# print("1")

# #1. create a pipeline object
# # clf = Pipeline([
# #     ('vectorizer_n_grams', CountVectorizer(ngram_range = (1, 2))),                  
# #     ('random_forest', (RandomForestClassifier()))         
# # ])

# # clf = Pipeline([
# #     ('vetorizer',CountVectorizer(ngram_range = (1,2))),
# #     ('Naive',MultinomialNB(alpha = 0.75))
# # ])

# # clf = Pipeline([
# #     ('vectorizer',TfidfVectorizer()),
# #     ('model',MultinomialNB(alpha = 0.75))
# # ])

def preProcess(text):
    doc = nlp(text)
    
    filtered_token = []
    
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        filtered_token.append(token.lemma_)
    
    return " ".join(filtered_token)


# print("2")

# #2. fit the pipeline object with the training data
# # X_train = []
# # y_train = []

# # for i in data:
# #     for j in data[i]:
# #         X_train.append(preProcess(j))
# #         y_train.append(i)

# # clf.fit(X_train, y_train)

# #3. predict the intent for new data

# # print(getIntent('Open music player.'))

import pickle
# # with open('nlu_model_test', 'wb') as f:
# #     pickle.dump(clf, f)
# # print("3")
with open('nlu_model_test', 'rb') as f:
    clf = pickle.load(f)

# # clf = m
def getIntent(text):    
    text = preProcess(text)
    return clf.predict([text])[0]


def finalModel(text):
    text = preProcess(text)
    prediction = getIntent(text)
    if prediction=='changeVolume':
        percentage = '10'
        doc = nlp(text)
        for token in doc:
            if token.is_digit:
                percentage = token
        return {'volume':str(percentage)},200

    if prediction=='openApp':
        apps = ['phone','contacts','settings','alarm','youtube','music player','music','musicplayer','photos','gallery','messages','clock','camera','calculator']
        doc = nlp(text)

        for token in doc:
            if str(token) in apps:
                return {'app':str(token)},200
    return {},404

print(finalModel('Open music player.'))