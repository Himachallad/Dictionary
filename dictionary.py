import json
from difflib import get_close_matches
import mysql.connector

con = mysql.connector.connect(
    user = "ardit700_student",
    password = "ardit700_student",
    host = "108.167.140.122",
    database = "ardit700_pm1database"
)


def findDictionaryWords():
    dictionary_words = []
    try:
        cursor = con.cursor()
        query = cursor.execute("SELECT Expression FROM Dictionary")
        results = cursor.fetchall()
        for result in results:
            dictionary_words.append(result[0])
        return dictionary_words
    except Exception:
        print("Couldn't connect to database")

def findWordMeaning(word):
    meanings = []
    try:
        cursor = con.cursor()
        query = cursor.execute("SELECT Definition FROM Dictionary where Expression='" + word + "'")
        results = cursor.fetchall()
        for result in  results:
            meanings.append(result[0])
        return meanings
    except Exception:
        print("Couldn't connect to database")

def _parseToDictionary():
    try:
        data = json.load(open("./data.json"))
        return data
    except FileNotFoundError:
        print("File doesn\'t exist")

dictionary = _parseToDictionary()

dictionary_expressions = findDictionaryWords()

def find_close_matches(word):
    return get_close_matches(word, dictionary_expressions, 1, 0.8)

def translate(word):
    word = word.lower()
    if word in dictionary_expressions:
        return dictionary[word]
    elif word.title() in dictionary_expressions: 
        return findWordMeaning(word.title())
    elif word.upper() in dictionary_expressions: 
        return findWordMeaning(word.upper())
    elif len(find_close_matches(word)) > 0:
        yn = input("Did you mean %s instead? Enter Y if yes or N if No." % find_close_matches(word)[0])
        if yn == "Y":
            return findWordMeaning(find_close_matches(word)[0])
        elif yn == "N":
            return "The word doesn't exist. Please double check it."
        else: 
            return "We didn't understand your entry"
    else:
        return "The word doesn't exist. Please double check it."
while True:
    word = input("Enter text to search:")
    output = translate(word)

    if isinstance(output, list):
        for item in output:
            print(item)
    else:
        print(output)