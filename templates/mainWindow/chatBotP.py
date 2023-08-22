import random
import json
import pickle
import numpy as np
import nltk
from tensorflow.keras.models import load_model
import spacy
import speech_recognition as sr
import pyttsx3
import serial
import struct


def wave_to_text(file_name):
    global r
    try:
        audio = sr.AudioFile(file_name)
        with audio as source:
            audio = r.record(source)
            result = r.recognize_google(audio, language='es-GT')
    except ImportError:
        result = "Lo siento, no pude entenderte"
    return result


# Lematizacíon
r = sr.Recognizer()
nlp = spacy.load('es_core_news_sm')


# Función para lematizar palabras
def lemmaSP(word):
    doc = nlp(word)
    for token in doc:
        lemma = token.lemma_
    return lemma


# Función para convertir de texto a audio
def tts(phrase):
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.say(phrase)
    engine.runAndWait()
    #del (engine)
    return


# Función para escribir en el puerto serial
def serialSend(state):
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM7'
    ser.open()
    ser.write(struct.pack('>B', state))
    ser.close()
    return


# Recuperación de listas, diccionario y modelo entrenado
intents = json.loads(open('templates/dataSettingWindow/TF/intentsUVG.json',
                          encoding="utf-8").read())
words = pickle.load(open('templates/dataSettingWindow/TF/wordsUVG.pkl', 'rb'))
classes = pickle.load(open('templates/dataSettingWindow/TF/classesUVG.pkl',
                           'rb'))
model = load_model('templates/dataSettingWindow/TF/chatbotmodelUVG.h5')


# Genera una lista con las palabras de la entrada lematizadas
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmaSP(word.lower()) for word in sentence_words]
    return sentence_words


# Limpia la oración de entrada y elimina los elementos repetidos
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


# Predicción de clase
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    print("traduciendo")
    ERROR_TRESHOLD = 0.2
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_TRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


# Obtención de una respuesta
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result
