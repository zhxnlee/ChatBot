import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from training import train_model
import discord
intents = discord.Intents.all()
client = discord.Client(intents=intents)


lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


# def get_response(intents_list, intents_json):
#     tag = intents_list[0]['intent']
#     list_of_intents = intents_json['intents']
#     for i in list_of_intents:
#         if i['tag'] == tag:
#             result = random.choice(i['responses'])
#             break
#     return result

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']

    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            if float(intents_list[0]['probability']) < 0.8:
                result = "I'm sorry, I don't understand you."
            break
    return result

print(classes)
def add_training_data():
    print("Enter the new tag for the training data: ")
    tag = input("")

    patterns = []
    print("Enter the patterns for the training data (one at a time, enter 'done' to finish): ")
    pattern = input("")
    while pattern.lower() != "done":
        patterns.append(pattern)
        pattern = input("")

    responses = []
    print("Enter the responses for the training data (one at a time, enter 'done' to finish): ")
    response = input("")
    while response.lower() != "done":
        responses.append(response)
        response = input("")

    intents['intents'].append({
        "tag": tag,
        "patterns": patterns,
        "responses": responses
    })
    with open('intents.json', 'w') as file:
        json.dump(intents, file)
    train_model()

def testchat():
    message = input("Input: ")
    ints = predict_class(message)
    res = get_response(ints, intents)
    print(res)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return
    if message.channel.name == 'general':
        if user_message[0] == '$':

            ints = predict_class(user_message)
            print(ints)
            res = get_response(ints, intents)
            print(res)
            await message.channel.send(res[0].upper() + res[1:len(res)])



client.run('MTEwNjM5MzM1NjYxMjkyNzUwOQ.G9oWgg.dbzttOtD7MILqETrTliWAlbeQF14afGywVan78')

#testchat()