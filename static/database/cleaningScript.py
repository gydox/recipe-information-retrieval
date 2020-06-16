import json, nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('stopwords')
f = open('data.json', "r")
data = json.loads(f.read())

wordnet_lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'[a-z]+')
stop_words = set(stopwords.words('english'))

# used to clean ingredients
# words that has other meaning if scrapped (needs to be removed
other_words = [
    'seeded'
]

measurement_word = [
    'cup', 'teaspoon', 'tablespoon', 'degree', 'f', 'c', 'need', 'optional', 'taste', 'cut', 'thin', 'thinly', 'finely',
    'slice', 'strip', 'shred', 'ounce', 'sheet', 'freeze', 'woody', 'base', 'remove', 'room', 'temperature',
    'inch', 'container', 'divide', 'half', 'lengthwise', 'halve', 'vertically'
]

preserve_word ={
    'shorten': 'shortening'
}


def preprocessText(document):
    document = document.lower()  # Convert to lowercase
    words = tokenizer.tokenize(document)  # Tokenize
    words = [w for w in words if not w in stop_words]  # Removing stopwords
    words = [w for w in words if not w in other_words]  # Removing other words

    # Lemmatizing
    for pos in [wordnet.NOUN, wordnet.VERB, wordnet.ADJ, wordnet.ADV]:
        words = [wordnet_lemmatizer.lemmatize(x, pos) for x in words]

    words = [w for w in words if not w in measurement_word]  # Removing measurement words
    words = [preserve_word[w] if w in preserve_word.keys() else w for w in words]  # Removing measurement words
    return " ".join(words)


def segmentJson(docCount):
    newData = {}
    count = 0

    for key, value in data.items():
        newData.update({key: value})
        count = count + 1

        if count == docCount:
            break

    print(len(newData))

    jsonData = json.dumps(newData, indent=4)
    with open("data" + str(docCount) + ".json", "w") as outfile:
        outfile.write(jsonData)


def cleanIngredient():
    newData = {}

    for key, value in data.items():
        for i in range(len(value['ingredients'])):
            value['cleanIngredients'][i] = preprocessText(value['ingredients'][i])
            newData.update({key: value})

    jsonData = json.dumps(newData, indent=4)
    with open("cleanedData.json", "w") as outfile:
        outfile.write(jsonData)

cleanIngredient()