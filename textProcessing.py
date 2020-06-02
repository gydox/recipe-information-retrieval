import os, json, csv
from flask import Flask, app

import pandas as pd
import numpy as np

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')

from scipy.spatial.distance import cosine


wordnet_lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'[a-z]+')
stop_words = set(stopwords.words('english'))


def preprocessText(document):
    document = document.lower()  # Convert to lowercase
    words = tokenizer.tokenize(document)  # Tokenize
    words = [w for w in words if not w in stop_words]  # Removing stopwords
    # Lemmatizing
    for pos in [wordnet.NOUN, wordnet.VERB, wordnet.ADJ, wordnet.ADV]:
        words = [wordnet_lemmatizer.lemmatize(x, pos) for x in words]
    return " ".join(words)


# This is a function to generate query_rep
def lsa_query_rep(query):
    query_rep = []
    for x in preprocessText(query).split():
        try:
            vectorised_vocabulary = vectorizer.vocabulary_[x]
            query_rep.append(vectorised_vocabulary)
        except:
            print("no matching term")

    query_rep = np.mean(terms_rep[query_rep], axis=0)
    return query_rep


# This function get result by rank by _id
def getResults(query):
    query_rep = lsa_query_rep(query)
    query_doc_cos_dist = [cosine(query_rep, doc_rep) for doc_rep in docs_rep]
    print("here ", query_doc_cos_dist)
    query_doc_sort_index = np.argsort(np.array(query_doc_cos_dist))

    csvData = pd.read_csv(csvFilename)
    for index in range(len(query_doc_sort_index)):
        query_doc_sort_index[index] = csvData.iloc[query_doc_sort_index[index]][0]

    return query_doc_sort_index

app = Flask(__name__)
app.config['SECRET_KEY'] = 'allrecipe'
filename = os.path.join(app.static_folder, 'database', 'mockData2.json')

with open(filename) as file:
    recipeData = json.load(file)

row = []
text = ""

csvFilename = os.path.join(app.static_folder, 'database', 'recipeData.csv')

with open(csvFilename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['_id', 'text', 'processedText'])
    for _id, recipe in recipeData.items():
        text = recipe['dishName'] + " " + " ".join(recipe['ingredients'])
        writer.writerow([_id, text, preprocessText(text)])


from sklearn.feature_extraction.text import TfidfVectorizer

csvData = pd.read_csv(csvFilename)

vectorizer = TfidfVectorizer()
TF_IDF_matrix = vectorizer.fit_transform(csvData['processedText'])
print(TF_IDF_matrix.todense())
TF_IDF_matrix = TF_IDF_matrix.T

print('Vocabulary Size : ', len(vectorizer.get_feature_names()))
print('Shape of Matrix : ', TF_IDF_matrix.shape)
print(TF_IDF_matrix)
print(vectorizer.get_feature_names())

# Applying SVD
U, s, VT = np.linalg.svd(TF_IDF_matrix.toarray()) # .T is used to take transpose and .toarray() is used to convert sparse matrix to normal matrix

K = 2 # K is the number of components
TF_IDF_matrix_reduced = np.dot(U[:,:K], np.dot(np.diag(s[:K]), VT[:K, :]))

# Getting Document and term representation
terms_rep = np.dot(U[:,:K], np.diag(s[:K]))
# M X K matrix where M = Vocabulary Size and N = Number of documents

docs_rep = np.dot(np.diag(s[:K]), VT[:K, :]).T # N x K matrix

print(terms_rep)
print("docrep:")
print(docs_rep)
testQuery = lsa_query_rep("aa salmon bb sushi")
testResult = getResults("aa tuna")
print("test query", testQuery)
print("testResult", testResult)
