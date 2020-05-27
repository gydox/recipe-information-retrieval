from __future__ import division
from flask import Flask, request, render_template, json, app, redirect
from forms import SearchBar
import json

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

for key, value in recipeData.items():
    print(value)

# print(recipeData[2]['dishName'])

# for item in resultData:
#     print(item)
#     dishName = item['dishName']
#     ingredients = ' '.join(item['ingredients'])
#     print("dishname " + dishName)
#     print("ingredients " + ingredients)
#     data.append(dishName + " " + ingredients)
#
# print('printing data')
# print(data)


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
    processed_query = search_query.upper()
    return render_template(
        'results.html',
        recipeData=recipeData,
        search_query=search_query,
        exclude_query=exclude_query,
        processed_query=processed_query,
        form=search_form)


@app.route('/recipe/<int:_id>', methods=["POST", "GET"])
def recipe(_id):
    search_form = SearchBar()
    print("page_id: " + str(_id))
    recipe_id = request.form['recipe_id']
    print("request_id " + recipe_id)
    return render_template('recipe.html', _id=_id, recipe=recipeData[str(_id)], form=search_form)


if __name__ == "__main__":
    app.run(debug=True)
