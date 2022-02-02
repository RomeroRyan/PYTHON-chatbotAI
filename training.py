# What Does This File Do?
#   this file is run before main and used to train the bot with the dataset in
#   the json file. Everytime dataset is modified, the bot must be re-trained. Only
#   need to run this file once to create the AI model. (rerun if dataset is modified)
import random
import json
import pickle
import numpy as np                              # Must install library via command line
import nltk                                     # Must install library via command line
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential  # Must install library via command line
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
lemmatizer = WordNetLemmatizer()


# Open json file and load in the dataset into variable "data"
with open("intents.json") as file:
    data = json.load(file)

# create lists. (Dataset from json file will be organized into these lists)
words = []              # will hold a complete list of keywords ('keywords' in json)
topics = []            # hold a list of all the topics in the json file
docs = []               # dictonary of topics and their coresponding list of keywords (topics/keyword)
ignore_characters = ['?', '!', '.', ',']

# parse through the data and save it into lists
for intent in data["intents"]:                      # parse every "topic" chunk
    for keyword in intent["keywords"]:              # grabs list of words in "keywords" of current "topic"
        word_List = nltk.word_tokenize(keyword)     # tokenize words
        words.extend(word_List)                     # add it to a complete list of words
        docs.append((word_List, intent["topic"]))     # assigns current list of words to the current "topic" (greetings = hello, hey, whats up, ...)

    # saves list of "topics"
    if intent["topic"] not in topics:                # (topics = greetings, bye, advising, ...)
        topics.append(intent["topic"])

# lematize (stem) "words" and remove duplicates in lists 'words" and "topics"
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_characters]
words = sorted(set(words))
topics = sorted(set(topics))

# create files to save "words" and "topics" lists
pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(topics, open("topics.pkl", "wb"))

# CHECKPOINT:
#   So far, we have a complete List-of-root-Words that function like keywords.          ("words" list)
#   We also have a List-of-topics which are the header of each chunk in the json file.    ("topics" list)
#   We also have a list that connect a topic with it corresponding List-of-Keywords       ("doc" list)
# print("List of topics: ", topics, "\n")
# print("Complete list of Words:", words, "\n")
# print("Docs dictonary: ", docs, "\n")
# exit()


# PREPARE DATA FOR BOT TRAINING:
#   Will be using a one-hot encoded strategy. We will create a binary list the same size
#   as the complete list of words, each bit representing a word in that list.
#   We have list of words and character but need numerical values to feed to
#   the neural network which trains the AI bot.
training = []
output_Empty = [0] * len(topics)          # inital binary list of topics (topics)

for document in docs:                       # create bag of words
    bag = []
    word_keyword = document[0]              # document[0] = the list of key words of current topic
    word_keyword = [lemmatizer.lemmatize(w.lower()) for w in word_keyword]

    # compare each word in complete list of keywords to current topic's list of keywords
    for w in words:
        if w in word_keyword:               # IF: it exist in current topic's list of words, append 1
            bag.append(1)
        else:                               # ELSE: does not exist in current topic's list of words, append 0
            bag.append(0)

    output_Row = list(output_Empty)
    output_Row[topics.index(document[1])] = 1
    training.append([bag, output_Row])
    # print("current topic: ",document[1], " = ", output_Row, "\n")
    # print("Current topic's bag-of-words: ",word_keyword, " = ",  bag, "\n")

# CHECKPOINT:
#   Every topic and it's corresponding Bag-of-Words have been turn to binary lists.
#   example:
#       Words = {hello, goodbye, morning, advising, schedule}
#           Greetings Bag    = {1, 0, 1, 0, 0}
#           Farewell Bag     = {0, 1, 0, 0, 0}
#           Advising bag     = {0, 0, 0, 1, 1}
#
#       topics = {greetings, farewell, advising}
#           Greeting topic      = {1, 0, 0}
#           Advising topic      = {0, 0, 1}
#           Farewell topic      = {0, 1, 0}
#
#   We then save the binary topic and it corresponding binary Bag-of-Words into a
#   dictonary named 'training'
# print("Training Dictonary: ", training, "\n")
# exit()



# shuffle training data and converting it to array
random.shuffle(training)
training = np.array(training)

# spit training data into X (word bags) and Y (topics)
training_X = list(training[:, 0])
training_Y = list(training[:, 1])


# ---------------------------------------------------------------------------
# The AI (The neural network, copied from NeuralNine tutorial "Intelligent AI Chatbot")
#   todo: explain what going on

model = Sequential()
model.add(Dense(128, input_shape=(len(training_X[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(training_Y[0]), activation='softmax'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
myModel = model.fit(np.array(training_X), np.array(training_Y), epochs=200, batch_size=5, verbose=1)

# the AI has been train, save training model into a file that can now be access
model.save('chatbot_Model.h5', myModel)
print("---Done---")
