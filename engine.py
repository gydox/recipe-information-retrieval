from flask import Flask, app
import pickle, nltk, os, json, re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from collections import Counter
import textProcessing

# nltk.download('stopwords')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'allrecipe'

data = {}
clickthrough = {}

filename = os.path.join(app.static_folder, 'database', 'cleanedData.json')
with open(filename) as file:
    data = json.load(file)

filename = os.path.join(app.static_folder, 'database', 'clickthrough.json')
with open(filename) as file:
    clickthrough = json.load(file)

# f = open('cleanedData.json', "r")
# data = json.loads(f.read())

df = pd.DataFrame(columns=["id", "text"])

i = 0
for key, value in data.items():
    ingredient_text = ' '.join(value["cleanIngredients"])
    dish_name = textProcessing.preprocessText(value["dishName"])
    full_text = dish_name + " " + ingredient_text
    new_row = {'id': key, 'text': ingredient_text}
    df = df.append(new_row, ignore_index=True)
    i = i + 1

# vectorizing and removing stop words
tfidf = TfidfVectorizer(max_features=5000, stop_words=nltk.corpus.stopwords.words('english'))
X = tfidf.fit_transform(df.text)

# making sure all features have 0 mean and unit standard deviation
scaler = StandardScaler()
X = scaler.fit_transform(X.todense())


def get_keywords(X, tfidf, k=20):
    """
    X: is the features matrix
    tfidf: is the tfidf object used to vectorize the texts
    k: maximum number of keywords for each text
    """

    feature_names = tfidf.get_feature_names()
    keywords = []
    ponts_tfidf = []
    for i in range(X.shape[0]):
        text_vector = X[i]
        idxs = np.array(text_vector.argsort()[-k:][
                        ::-1]).T  # getting the index of the most important words (with more tfidf ponctuation)
        s = ''
        for j in range(k):
            # sometimes 100 keywords are too much, so I make sure I don't get useless words
            if text_vector[idxs[j]] != 0:
                s = s + feature_names[idxs[j]]
                if j != k - 1:
                    s = s + ','
        keywords.append(s)
    return keywords


def search_keyword(df, user_keywords: list, user_exclude_keywords: list = []):
    idxs = []
    for user_keyword in user_keywords:
        bools = df.keywords.apply(lambda x: user_keyword in x)  # does this text have this keyword?
        idxs.extend(list(df.keywords.loc[bools].index))  # keeps track of the texts that have the keywords

    # counts how many of the keywords each text has
    counter = {k: v for k, v in sorted(dict(Counter(idxs)).items(), key=lambda item: item[1], reverse=True)}

    # initialize the output of the function. I'll append to this empty dataframe
    df_out = pd.DataFrame(columns=['id', 'text', 'keywords'])
    user_keywords_text = []
    for idx, count in zip(counter.keys(), counter.values()):
        aux = df.loc[idx][['id', 'text', 'keywords']]

        # excluding keywords
        full_text_string = ','.join(aux.text.split(' '))
        # print("keyword:",df.loc[idx]['id'],":",df.loc[idx]['keywords'])
        # print(full_text_string)
        excluding = False
        if user_exclude_keywords != ['']:
            print("yes, condition met")
            for exclude_word in user_exclude_keywords:
                if exclude_word in full_text_string:
                    print("excluding: ", exclude_word, " at id: ",df.loc[idx]['id'], ":", full_text_string)
                    excluding = True
                    break
        # end exclude keyword

        if not excluding:
            print("not really excluding this ", df.loc[idx]['id'])
            s = [user_keyword for user_keyword in user_keywords if user_keyword in df.loc[idx]['keywords']]
            s = ','.join(s)
            user_keywords_text.append(s)

            df_out = df_out.append(aux)
            print("appended:", df.loc[idx]['id'])
        else:
            print("excluded ", df.loc[idx]['id'], 'excluding :')

    df_out.reset_index(inplace=True)
    del df_out['index']
    df_out.columns = ['id', 'text', 'keywords']
    df_out['match'] = user_keywords_text

    # print(df_out.loc[0])
    # print(df_out.loc[0].text)
    # print(df_out.loc[0].keywords)
    # print(df_out.loc[1])
    # print(df_out.loc[2])
    # print(df_out.loc[3])

    return df_out


def account_clickthrough(query_keywords, result_list, clickthrough):
    id_score = {}
    result = []
    for keyword, _ids in clickthrough.items():
        for query_keyword in query_keywords:
            if query_keyword == keyword:
                for _id, score in _ids.items():
                    # Increment score in dictionary
                    id_score[_id] = id_score.get(_id, 0) + score

    # Sort id_score dictionary from highest to lowest score
    for _id, score in sorted(id_score.items(), key = lambda kv:(kv[1], kv[0]), reverse=True):
        if _id in result_list:
            result.append(_id)

    for _id in result_list:
        if _id in result:
            continue
        else:
            result.append(_id)

    # print(result)
    return result


def update_clickthrough(query_keywords, _id, clickthrough):
    for keyword in query_keywords:
        if keyword in clickthrough.keys():
            clickthrough[keyword][_id] = clickthrough.get(keyword, 0).get(_id, 0) + 1
        else:
            clickthrough.update({keyword: {_id:1}})

    # print(clickthrough)
    filename = os.path.join(app.static_folder, 'database', 'clickthrough.json')
    with open(filename, 'w') as write_file:
        json.dump(clickthrough, write_file, indent=4)


# result_list = ['222222', '280228', '278988']
# account_clickthrough(query_keywords=['chicken', 'rice'], result_list=result_list, clickthrough=clickthrough)
# update_clickthrough(query_keywords=['banana'], _id='123', clickthrough=clickthrough)

keywords = get_keywords(X, tfidf)
df["keywords"] = keywords

# list with all the keywords you are interested in. Only single lower case words
# user_keywords = ['potato', 'chip']
# user_exclude_keywords=[]
# df_out = search_keyword(df=df, user_keywords=user_keywords, user_exclude_keywords=user_exclude_keywords )
#
# print(df_out.loc[0])
# print(df_out.loc[1])
# print(df_out.loc[2])
# print(df_out.loc[3])
