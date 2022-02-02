# AI Class Project: CSUF Portal Bot
# Peter Bergeon, Brian Edwards, Ryan Romero

# ----- Libraries -----
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

# ----- Setup -----
lemmatizer = WordNetLemmatizer()

with open("intents.json") as file:
    data = json.load(file)

words = pickle.load(open("words.pkl", "rb"))
topics = pickle.load(open("topics.pkl", "rb"))
model = load_model("chatbot_Model.h5")


# ----- Helper Functions -----

# clean_up_sentences:
#       lowercase and stems(root) user's string
def clean_up_sentences(userString):
    sentence = nltk.word_tokenize(userString)
    sentence = [lemmatizer.lemmatize(word.lower()) for word in sentence]
    return sentence

# bag_of_words:
#       convert user's string to a bag-of-words. A list of 0s and 1s that indiciate
#       if a word exist in the complete-list-of-words saved in training.py
def bag_of_words(userString):
    sentence = clean_up_sentences(userString)
    bag = [0]* len(words)
    for w in sentence:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

# chatBot:
#       Gives a user's string a percentage value for each topic in json file
#       we will check to see if percentage chance is greater then 75%
#       if so, we will assume the question is that of the json topic and respond
#       if below 75%, bot will print out a "I dont understand" message
def chatBot(userString):
    currentBag = bag_of_words(userString)
    result = model.predict(np.array([currentBag]))[0]
    # print("Result: ", result, "\n")


    # get the highest numerical value prediction
    result_index = np.argmax(result)
    # print("Highest Result Index: ", result_index, "\n")

    # get the topic associated to the highest numerical value prediction
    topic = topics[result_index]

    # IF: percentage is greater then 75%
    if result[result_index] > 0.80:
        # we grab the list of responds and choose one at random
        for tg in data["intents"]:
            if tg["topic"] == topic:
                responses = tg['responses']
        print(random.choice(responses))

    # ELSE: we print out a confused bot response
    else:
        print("Sorry, I didn' understand. Try asking again.")




# ----- Main -----
while True:
    print("-------------------------------------------------------------------")
    userString = input("You: ")
    print(" ")
    chatBot(userString)
