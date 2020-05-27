# Food recipe search engine
Search engine on recipe data to test information retrieval algorithm. Food recipe topic is choosen becuase there are many creative ways a user can query for a food recipe. For example, a use can search by dish name or ingredients. This topic also gives challenge when a user wants to exclude an ingredient in a query. For example, a person might want to exclude peas from the ingredient would search for "pie without peas".

## Data Source
Data is scrapped from allrecipe.com using Beautiful Soup 4.

## Information Retriecal Algorithm
### Term Frequency - Inverse Term Frequency (TF-IDF)
We will be using TF-IDF algorithm as we will have a large dataset of recipes. TF-IDF will be a good algorithm to use in this case to calculate the importance of a keyword by comparing its frequency in the page to the same keyword frequency in a large set of documents.

### Boolean model 
Boolean model will be built into the UI to solve a specific problem when users wants to query a recipe excluding one or more ingredient.

### Relevance Feedback
Relevance feedback model will be implemented into the search algorithm to increase search relevance. This is so that we can tackle the issue where the recipe document does not include a term that it is supposed to be included. For example, the recipe “Eggs Benedict” is a breakfast meal but will not appear if the user queries for “breakfast”. Therefore a relevance feedback model such as click through can solve this issue after the system is naturally used over a period of time.

## Local Development
### Prerequisits
- Python 3.7
- pip3

### Scripts
1. Clone this repository
2. Download dependencies
```pip3 install -r requirements.txt```
3. Run main.py
```python3 main.py```
4. open localhost in browser
```http://127.0.0.1:5000/```
