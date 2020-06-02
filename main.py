from __future__ import division
from flask import Flask, request, render_template, json, app, redirect

import textProcessing
from forms import SearchBar
import json
import textProcessing

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import Counter

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'allrecipe'


recipeData = {}

# static/database/mockData.json
filename = os.path.join(app.static_folder, 'database', 'mockData2.json')
with open(filename) as file:
    # jsonFile = json.load(file)
    # recipeData = jsonFile['recipeData']
    recipeData = json.load(file)
    print(recipeData)


def sortJsonResult(rank_ids):
    rankedResultData = {}
    print("printing ranked ids: ", rank_ids)
    for i in range(len(rank_ids)):
        # recipeItem = {
        #     str(rank_ids[i]): recipeData[str(rank_ids[i])]
        # }
        print("key: ", str(rank_ids[i]))
        print("value: ", recipeData[str(rank_ids[i])])
        rankedResultData[str(rank_ids[i])] = recipeData[str(rank_ids[i])]
        # rankList.append(recipeItem)

    # rankedResultData = json.dumps(rankList)
    return rankedResultData


@app.route('/', methods=["POST", "GET"])
def index():
    # with app.open_recource('mockData.json') as f:
    #     contents = f.read()
    #     print(contents)
    #     data = json.load(f)
    #     print(data)
    #
    # resultData = data['resultData']

    search_form = SearchBar()
    return render_template('index.html', form=search_form)


@app.route('/results', methods=["POST"])
def results():
    search_form = SearchBar()
    search_query = request.form['query']
    exclude_query = request.form['exclude']
    print(search_query)
    processed_query = textProcessing.preprocessText(search_query)

    result_rank_ids = textProcessing.getResults(search_query)
    result_rank = sortJsonResult(rank_ids=result_rank_ids)

    # print("result rank: ", result_rank)
    # for key, value in result_rank.items():
    #     print(key, ": ", value)

    return render_template(
        'results.html',
        recipeData=result_rank,
        search_query=search_query,
        exclude_query=exclude_query,
        processed_query=processed_query,
        form=search_form,
    )


@app.route('/recipe/<int:_id>', methods=["POST", "GET"])
def recipe(_id):
    search_form = SearchBar()
    print("page_id: " + str(_id))
    recipe_id = request.form['recipe_id']
    print("request_id " + recipe_id)
    return render_template('recipe.html', _id=_id, recipe=recipeData[str(_id)], form=search_form)


if __name__ == "__main__":
    app.run(debug=True)
