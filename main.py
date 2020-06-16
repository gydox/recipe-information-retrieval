from __future__ import division
from flask import Flask, request, render_template, json, app, redirect

import textProcessing
from forms import SearchBar
import json
import textProcessing
import engine

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import Counter

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'allrecipe'


recipeData = {}
filename = os.path.join(app.static_folder, 'database', 'cleanedData.json')
with open(filename) as file:
    recipeData = json.load(file)


def sortJsonResult(rank_ids):
    rankedResultData = {}
    for i in range(len(rank_ids)):
        rankedResultData[str(rank_ids[i])] = recipeData[str(rank_ids[i])]

    return rankedResultData


@app.route('/', methods=["POST", "GET"])
def index():
    search_form = SearchBar()
    return render_template('index.html', form=search_form)


@app.route('/results', methods=["POST"])
def results():
    search_form = SearchBar()
    search_query = request.form['query']
    exclude_query = request.form['exclude']
    processed_exclude_query = textProcessing.preprocessText(exclude_query)
    processed_query = textProcessing.preprocessText(search_query)
    query_list = processed_query.split(' ')
    exclude_list = processed_exclude_query.split(' ')
    print('ex: ', exclude_list)
    result_rank_ids = engine.search_keyword(df=engine.df, user_keywords=query_list, user_exclude_keywords=exclude_list).id.to_numpy()
    print("res rank id:", result_rank_ids)
    result_rank_ids = engine.account_clickthrough(query_keywords=query_list, result_list=result_rank_ids, clickthrough=engine.clickthrough)

    result_rank = sortJsonResult(rank_ids=result_rank_ids)

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
    recipe_id = request.form['recipe_id']
    processed_query = request.form['processed_query']
    query_list = processed_query.split(' ')
    engine.update_clickthrough(query_keywords=query_list, _id=recipe_id, clickthrough=engine.clickthrough)
    return render_template('recipe.html', _id=_id, recipe=recipeData[str(_id)], form=search_form)


if __name__ == "__main__":
    app.run(debug=True)
