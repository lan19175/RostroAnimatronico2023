import random
import json
# Librerias
import pickle
import numpy as np
import nltk
# from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
# from tensorflow.keras.utils import plot_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import spacy
# from spacy import displacy
# se carga el lematizador
nlp = spacy.load('es_core_news_sm')


def runTraining():
    # Funcion para lematizar palabras
    
    def lemmaSP(word):
        doc = nlp(word)
        for token in doc:
            lemma = token.lemma_
        return lemma
    # Se lee el archivo JSON
    intents = json.loads(open('templates/dataSettingWindow/TF/intentsUVG.json',
                              encoding="utf-8").read())

    words = []
    classes = []
    documents = []
    ignore_letters = ['?', '!', '.', ',']

    # Se extraen los datos del diccionario intents para formar
    # las listas que contienen las clases y palabras de los patrones
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            for i in ignore_letters:
                if i in words:
                    words.remove(i)
            documents.append((word_list, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    mc = []
    list1 = words

    # Se convierten todas las palabras de la lista en minusculas
    for i in list1:
        mc.append(lemmaSP(i.lower()))

    # Se ordenan y se eliminan palabras repetidas
    words = mc
    words = sorted(set(words))
    classes = sorted(set(classes))

    # Se serializan las listas "words" y "classes" para el chatbot
    pickle.dump(words, open('templates/dataSettingWindow/TF/wordsUVG.pkl',
                            'wb'))
    pickle.dump(classes, open('templates/dataSettingWindow/TF/classesUVG.pkl',
                              'wb'))

    training = []
    output_empty = [0]*len(classes)

    # Se crea la matriz de entrenamiento del modelo
    for document in documents:
        bag = []
        word_patterns = document[0]
        # Lista con las palabras de cada patron lematizadas y en minusculas
        word_patterns = [lemmaSP(word.lower()) for word in word_patterns]
        for word in words:
            # Lista que indica las palabras encontradas en cada patron de la
            # lista de palabras
            bag.append(1) if word in word_patterns else bag.append(0)
        output_row = list(output_empty)
        # Lista que indica a que clase pertenece la frase anterior
        output_row[classes.index(document[1])] = 1
        # Lista de entrenamiento con las frases convertidas y la clase a la
        # que pertenece se desordena aleatoriamente para evitar sesgos
        training.append([bag, output_row])
    random.shuffle(training)
    training = np.array(training)

    train_x = list(training[:, 0])  # Patrones ya codificados
    train_y = list(training[:, 1])  # Clases codificados

    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd, metrics=['accuracy'])

    hist = model.fit(np.array(train_x), np.array(train_y),
                     epochs=200, batch_size=5, verbose=1)
    model.save('templates/dataSettingWindow/TF/chatbotmodelUVG.h5', hist)
    print("Done")
