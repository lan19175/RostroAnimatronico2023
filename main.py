import json
import cv2
import pyaudio
import wave
import time
import random

from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty, NumericProperty
from threading import Thread, Event
from functools import partial
from tensorflow.keras.models import load_model
from keras.utils import img_to_array
import numpy as np

import templates.mainWindow.chatBotP as chatbot
# import Trainer

# variables a utilizar
dummy = 0
bandera_camara_seleccion = 0
camara_selected = 0
chatbot_new_messege = 0
hablando = 0
modo_intelifencia = 0  # 0 = chatbot, 1 = chatGPT
frames = []

evento = Event()
hablar = Event()
video = Event()
evento.clear()
hablar.clear()
video.clear()

# variables para crear el archivo de audio
formato = pyaudio.paInt16
canales = 1
ratio = 44100
chunk = 1024
wave_name = "templates/mainWindow/usuario_speech.wav"

# visión por computadora
face = "templates/mainWindow/emotion_detector/haarcascade.xml"
emotion = "templates/mainWindow/emotion_detector/EmotionDetectionModelElu5.h5"
face_cascade = cv2.CascadeClassifier(face)
classifier = load_model(emotion)
emotion_label = ['Enojo',
                 'Disgusto',
                 'Miedo',
                 'Alegria',
                 'Neutral',
                 'Triste',
                 'Sorpresa']

# resolución aplicacion
Window.maximize()

# carga de archivos .kv
Builder.load_file('templates/manager_window.kv')
Builder.load_file('templates/mainWindow/main_window.kv')
Builder.load_file('templates/dataSettingWindow/data_setting_window.kv')
Builder.load_file('templates/dataSettingWindow/append_chatbot_window.kv')
Builder.load_file('templates/motorWindow/motor_window.kv')
Builder.load_file('templates/motorWindow/emoji_window.kv')
Builder.load_file('templates/settingsWindow/settings_popup.kv')


class WindowManager(ScreenManager):
    pass


# gestos guardados en MotorWindow
class EmojiOptions(BoxLayout):
    name = StringProperty()
    emoji_link = StringProperty()
    M1 = NumericProperty()
    M2 = NumericProperty()
    M3 = NumericProperty()
    M4 = NumericProperty()
    M5 = NumericProperty()
    M6 = NumericProperty()
    M7 = NumericProperty()
    M8 = NumericProperty()
    M9 = NumericProperty()
    M10 = NumericProperty()
    M11 = NumericProperty()
    M12 = NumericProperty()
    M13 = NumericProperty()
    M14 = NumericProperty()
    M15 = NumericProperty()
    M16 = NumericProperty()
    M17 = NumericProperty()
    M18 = NumericProperty()
    M19 = NumericProperty()

    def emoji_press(self):
        global motor_window
        motor_window.ids.control_emojis.image_source = self.emoji_link
        for i in range(19):
            id_slider = "manual_servo" + str(i)
            m_value = "M" + str(i+1)
            motor_window.ids[str(id_slider)].slider_val = getattr(self,
                                                                  str(m_value))

    def delete_emoji(self):
        global motor_window
        file_path = 'templates/motorWindow/emoji_data.json'
        emoji_json = open(file_path)
        data = json.load(emoji_json)
        indexx = 0
        for emoji in data['emojis_details']:
            if self.name == emoji["nombre"]:
                del data['emojis_details'][indexx]
                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, indent=4)
            else:
                indexx += 1
        motor_window.ids.emoji_options.clear_widgets()
        for emoji in data['emojis_details']:
            emoji_name = str(emoji["emoji"])
            emoji_link_str = ('templates/motorWindow/imagenes/emojis/'
                              + emoji_name + '.png')
            new = EmojiOptions(
                name=emoji["nombre"],
                emoji_link=emoji_link_str,
                M1=emoji["M1"],
                M2=emoji["M2"],
                M3=emoji["M3"],
                M4=emoji["M4"],
                M5=emoji["M5"],
                M6=emoji["M6"],
                M7=emoji["M7"],
                M8=emoji["M8"],
                M9=emoji["M9"],
                M10=emoji["M10"],
                M11=emoji["M11"],
                M12=emoji["M12"],
                M13=emoji["M13"],
                M14=emoji["M14"],
                M15=emoji["M15"],
                M16=emoji["M16"],
                M17=emoji["M17"],
                M18=emoji["M18"],
                M19=emoji["M19"])
            motor_window.ids.emoji_options.add_widget(new)


# popup para seleccion de emoji
class EmojiWindow(Popup):
    def emoji_selected(self, emoji_id):
        global motor_window
        emoji_source = ('templates/motorWindow/imagenes/emojis/'
                        + emoji_id
                        + '.png')
        motor_window.ids.emoji.image_source = emoji_source
        motor_window.ids.emoji.emoji_selected = emoji_id


# popup de settings
class SettingWindow(Popup):
    def spinner_clicked(self, value):
        global camara_selected, bandera_camara_seleccion

        if (value == "Internal Camara"):
            camara_selected = 0
        else:
            camara_selected = 1
        bandera_camara_seleccion = 1

    def values_array(self):
        available_cameras_label = ["Internal Camara", "USB Camara"]
        return available_cameras_label

    def conectar_com(self):
        pass


class MensajeCelularChatbot(Button):
    texto = StringProperty()
    ancho = NumericProperty()
    altura = NumericProperty()


class MensajeCelularUsuario(Button):
    texto = StringProperty()
    ancho = NumericProperty()
    altura = NumericProperty()


# ventana principal
class MainWindow(Screen):
    def on_pre_enter(self):
        global main_window
        main_window = self
        video.set()

    def on_pre_leave(self):
        source = 'templates/mainWindow/imagenes/robot_neutral.png'
        self.ids.chatbot_estado.source = source
        self.ids.photo.reload()
        source = 'templates/mainWindow/imagenes/photo/sin_emoji.png'
        video.clear()
        self.ids.emoji_photo.source = source

    def emotion_detection(self):
        global cam, label, bandera_camara_seleccion, camara_selected
        cam = cv2.VideoCapture(0)
        while (1):
            if (bandera_camara_seleccion == 1):
                cam.release()
                cam = cv2.VideoCapture(camara_selected)
                bandera_camara_seleccion = 0

            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray,
                                      (48, 48),
                                      interpolation=cv2.INTER_AREA)
                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    preds = classifier.predict(roi)[0]
                    label = emotion_label[preds.argmax()]
                    cv2.putText(frame,
                                label,
                                (x-10, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                2,
                                (255, 255, 255),
                                2)
                else:
                    cv2.putText(frame,
                                'No Face Found',
                                (20, 20),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                2,
                                (0, 0, 255),
                                3)
            Clock.schedule_once(partial(self.display_frame, frame))
            cv2.waitKey(1)
            video.wait()
        cam.release()
        cv2.destroyAllWindows()

    def display_frame(self, frame, dt):
        global main_window
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]),
                                 colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(order=None),
                            colorfmt='bgr',
                            bufferfmt='ubyte')
        texture.flip_vertical()
        main_window.ids.vid.texture = texture

    def chat_bot_talk(self):
        while (1):
            global res, hablando
            if (hablando == 1):
                chatbot.tts(res)
                time.sleep(.5)
                hablando = 0
                hablar.clear()
            hablar.wait()

    def chat_bot_do(self):
        while (1):
            global dummy, frames, evento, stream, user_ask, chatbot_new_messege
            if dummy == 1:
                data = stream.read(chunk)
                frames.append(data)
            elif dummy == 2:
                global res
                try:
                    ints = chatbot.predict_class(user_ask)
                    bandera_ints = 1
                except ImportError:
                    bandera_ints = 0
                if (bandera_ints == 1):
                    if (float(ints[0]['probability']) >= 0.7):
                        try:
                            res = chatbot.get_response(ints, chatbot.intents)
                        except ImportError:
                            res = "Lo siento, no pude entenderte"
                        time.sleep(0.1)
                        chatbot_new_messege = 1
                    else:
                        res = "Lo siento, no pude entenderte"
                        time.sleep(0.1)
                        chatbot_new_messege = 1
                else:
                    res = "Lo siento, no pude entenderte"
                    chatbot_new_messege = 1
                time.sleep(0.05)
            evento.wait()

    def show_picture(self):
        global cam, main_window, label, hablando, res
        ret, frame = cam.read()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]),
                                 colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(order=None),
                            colorfmt='bgr',
                            bufferfmt='ubyte')
        texture.flip_vertical()
        main_window.ids.photo.texture = texture
        source = 'templates/mainWindow/imagenes/photo/' + label + '.png'
        main_window.ids.emoji_photo.source = source
        file_path = 'templates/mainWindow/emotion_detector/respuestas.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            emotion_respuestas = json.load(json_file)
        for emotion in emotion_respuestas["emotions"]:
            if (emotion["tag"] == label):
                res = random.choice(emotion["responses"])
        hablando = 1
        hablar.set()

    def start(self):
        def start(dt):
            self.ids.countdown_label.text = "PREPARATE"
            self.ids.countdown_label.font_size = 50

        def countdown_one(dt):
            self.ids.countdown_label.text = "3"
            self.ids.countdown_label.font_size = 150

        def countdown_two(dt):
            self.ids.countdown_label.text = "2"

        def countdown_three(dt):
            self.ids.countdown_label.text = "1"

        def finish(dt):
            self.ids.countdown_label.font_size = 75
            self.ids.countdown_label.text = "CHEESE"
            self.show_picture()

        Clock.schedule_once(countdown_one, 1)
        Clock.schedule_once(countdown_two, 2)
        Clock.schedule_once(countdown_three, 3)
        Clock.schedule_once(finish, 3.5)
        Clock.schedule_once(start, 5.5)

    def cambio_inteligencia(self):
        global modo_intelifencia
        if (modo_intelifencia == 0):
            modo_intelifencia = 1
            path = 'templates/mainWindow/imagenes/switch_derecha.png'
            self.ids.inteligencia.image_source = path
            self.ids.nombre_inteligencia.text = "INTELIGENCIA \n  ARTIFICIAL"
            pos_actual = self.ids.nombre_inteligencia.pos
            pos_nueva = [pos_actual[0], pos_actual[1] + 10]
            self.ids.nombre_inteligencia.pos = pos_nueva

        elif (modo_intelifencia == 1):
            modo_intelifencia = 0
            path = 'templates/mainWindow/imagenes/switch_izquierda.png'
            self.ids.inteligencia.image_source = path
            self.ids.nombre_inteligencia.text = "RED NEURONAL"
            pos_actual = self.ids.nombre_inteligencia.pos
            pos_nueva = [pos_actual[0], pos_actual[1] - 10]
            self.ids.nombre_inteligencia.pos = pos_nueva

    def escuchando(self):
        global stream, audio, dummy, evento, frames, formato, canales
        global ratio, chunk
        audio = pyaudio.PyAudio()
        stream = audio.open(format=formato, channels=canales,
                            rate=ratio, input=True,
                            frames_per_buffer=chunk)
        frames = []
        dummy = 1
        evento.set()

    def finalizar_escuchar(self):
        global stream, audio, evento, user_ask, dummy, res, chatbot_new_messege
        global hablando, canales

        evento.clear()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        waveFile = wave.open(wave_name, 'wb')
        waveFile.setnchannels(canales)
        waveFile.setsampwidth(audio.get_sample_size(formato))
        waveFile.setframerate(ratio)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        text_to_speech = 0
        try:
            user_ask = chatbot.wave_to_text(wave_name)
            text_to_speech = 1
        except ImportError:
            user_ask = "Lo siento, no pude entenderte"
        if (text_to_speech == 1):
            self.add_mensaje_usuario(user_ask)
            dummy = 2
            evento.set()
            while (chatbot_new_messege != 1):
                pass
            evento.clear()
            dummy = 0
            chatbot_new_messege = 0
            self.add_mensaje_chatbot(res)
        else:
            evento.clear()
            dummy = 0
            self.add_mensaje_chatbot(user_ask)
            time.sleep(0.1)
            chatbot_new_messege = 0
        hablando = 1
        hablar.set()

    def new_mensaje(self, text):
        length = len(text)
        width = length * 12
        if (width > 350):
            width = 350
        texto_split = text.split(" ")
        texto_arreglado = ""
        lines = 1
        max_length = 29
        for palabra in texto_split:
            texto_arreglado_new = texto_arreglado + palabra + " "
            length_now = len(texto_arreglado_new)
            if (length_now > max_length):
                texto_arreglado = texto_arreglado + "\n" + palabra + " "
                lines = lines + 1
                max_length = max_length + 29
            else:
                texto_arreglado = texto_arreglado_new
        height = lines * 30
        return width, height, texto_arreglado

    def add_mensaje_usuario(self, text):
        [ancho, altura, texto_arreglado] = self.new_mensaje(text)
        new = MensajeCelularUsuario(texto=texto_arreglado,
                                    ancho=ancho,
                                    altura=altura)
        self.ids.celular.add_widget(new, index=0)
        self.ids.scrollview_celular.scroll_to(new)

    def add_mensaje_chatbot(self, text):
        global dummy
        [ancho, altura, texto_arreglado] = self.new_mensaje(text)
        new = MensajeCelularChatbot(texto=texto_arreglado,
                                    ancho=ancho,
                                    altura=altura)
        self.ids.celular.add_widget(new, index=0)
        self.ids.scrollview_celular.scroll_to(new)
        # dummy = 1


# objeto de servo en MotorWindow
class ManualServo(BoxLayout):
    file1 = "templates/motorWindow/imagenes/SG90/Servo_cuerpo.png"
    file2 = "templates/motorWindow/imagenes/SG90/Servo_movil_v2.png"

    min_val = StringProperty("0")
    max_val = StringProperty("180")
    servo_angle_text = StringProperty()
    servo_nombre = StringProperty("Servo 1")
    cuerpo_path = StringProperty(file1)
    movil_path = StringProperty(file2)
    servo_angle = NumericProperty()
    pos_x_brazo = NumericProperty(.48)
    pos_y_brazo = NumericProperty(.17)
    pos_x_text = NumericProperty(.467)
    pos_y_text = NumericProperty(.53)
    slider_val = NumericProperty()

    def slider_func(self, value):
        self.servo_angle = int(value)
        self.servo_angle_text = f'{int(value)}°'
        self.slider_val = int(value)


# MotorWindow, ventana control manual de motores
class MotorWindow(Screen):
    def on_pre_enter(self):
        global motor_window
        # valores iniciales de los servos
        motor_window = self
        initial_value = [131, 51, 104,
                         112, 74, 41,
                         118, 150, 99,
                         54, 170, 43,
                         195, 37, 250,
                         270, 115, 180,
                         300]
        for i in range(19):
            id = "manual_servo" + str(i)
            value = initial_value[i]
            self.ids[str(id)].slider_val = value
        # carga min y max de cada servo
        file_path = 'templates/dataSettingWindow/servos_data.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            servos_list = json.load(json_file)
        for servo in servos_list:
            id = "manual_servo" + servo["id"]
            self.ids[str(id)].min_val = str(servo["min"])
            self.ids[str(id)].max_val = str(servo["max"])
        # carga de emojis almacenados
        emoji_json = open('templates/motorWindow/emoji_data.json')
        data = json.load(emoji_json)
        self.ids.emoji_options.clear_widgets()
        for emoji in data['emojis_details']:
            emoji_name = str(emoji["emoji"])
            emoji_link_str = ('templates/motorWindow/imagenes/emojis/'
                              + emoji_name + '.png')
            new = EmojiOptions(
                name=emoji["nombre"],
                emoji_link=emoji_link_str,
                M1=emoji["M1"],
                M2=emoji["M2"],
                M3=emoji["M3"],
                M4=emoji["M4"],
                M5=emoji["M5"],
                M6=emoji["M6"],
                M7=emoji["M7"],
                M8=emoji["M8"],
                M9=emoji["M9"],
                M10=emoji["M10"],
                M11=emoji["M11"],
                M12=emoji["M12"],
                M13=emoji["M13"],
                M14=emoji["M14"],
                M15=emoji["M15"],
                M16=emoji["M16"],
                M17=emoji["M17"],
                M18=emoji["M18"],
                M19=emoji["M19"])
            self.ids.emoji_options.add_widget(new)

    def send_gesto(self):
        pass

    # creación objeto emoji con formato json
    def new_emoji_data(self, name, emoji, motores):
        json_string = {
            "nombre": name,
            "emoji": emoji,
            "M1": int(motores[0]),
            "M2": int(motores[1]),
            "M3": int(motores[2]),
            "M4": int(motores[3]),
            "M5": int(motores[4]),
            "M6": int(motores[5]),
            "M7": int(motores[6]),
            "M8": int(motores[7]),
            "M9": int(motores[8]),
            "M10": int(motores[9]),
            "M11": int(motores[10]),
            "M12": int(motores[11]),
            "M13": int(motores[12]),
            "M14": int(motores[13]),
            "M15": int(motores[14]),
            "M16": int(motores[15]),
            "M17": int(motores[16]),
            "M18": int(motores[17]),
            "M19": int(motores[18])
        }
        return json_string

    def guardar_emoji(self):
        name_emoji = self.ids.nombre.text
        emoji_selected = self.ids.emoji.emoji_selected
        self.ids.nombre.text = ""
        motor_values = []
        for i in range(19):
            id = "manual_servo" + str(i)
            motor_values.append(int(self.ids[str(id)].slider_val))
        # creacion objeto json con valores de motores
        new_emoji = self.new_emoji_data(name_emoji, emoji_selected,
                                        motor_values)
        # escritura en archivo json
        with open('templates/motorWindow/emoji_data.json', 'r+') as file:
            file_data = json.load(file)
            file_data["emojis_details"].append(new_emoji)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        emoji_link_str = ('templates/motorWindow/imagenes/emojis/'
                          + emoji_selected + '.png')
        # creación de boton para gesto en la ventana
        new = EmojiOptions(
                name=name_emoji,
                emoji_link=emoji_link_str,
                M1=motor_values[0],
                M2=motor_values[1],
                M3=motor_values[2],
                M4=motor_values[3],
                M5=motor_values[4],
                M6=motor_values[5],
                M7=motor_values[6],
                M8=motor_values[7],
                M9=motor_values[8],
                M10=motor_values[9],
                M11=motor_values[10],
                M12=motor_values[11],
                M13=motor_values[12],
                M14=motor_values[13],
                M15=motor_values[14],
                M16=motor_values[15],
                M17=motor_values[16],
                M18=motor_values[17],
                M19=motor_values[18])
        self.ids.emoji_options.add_widget(new)

    def menu_pos(self):
        window_size = Window.size
        x_pos = window_size[0] - 250
        pos = x_pos
        return pos


# objeto servo en MotorDataSettingWindow
class MinMaxServo(BoxLayout):
    file1 = "templates/motorWindow/imagenes/SG90/Servo_cuerpo.png"
    file2 = "templates/motorWindow/imagenes/SG90/Servo_movil_v2.png"

    min_val = StringProperty("0")
    max_val = StringProperty("180")
    servo_angle_text = StringProperty("90°")
    servo_nombre = StringProperty("Servo 1")
    cuerpo_path = StringProperty(file1)
    movil_path = StringProperty(file2)
    servo_angle = NumericProperty(90)
    pos_x_brazo = NumericProperty(.48)
    pos_y_brazo = NumericProperty(.17)
    pos_x_text = NumericProperty(.467)
    pos_y_text = NumericProperty(.53)

    # al presionar enter en las entradas de min o max se actualizan los valores
    def on_value(self, value, min_max):
        if min_max == "min":
            self.min_val = value
        else:
            self.max_val = value

    def slider_func(self, value):
        self.servo_angle = int(value)
        self.servo_angle_text = f'{int(value)}°'


class AppendChatbot(Popup):
    def append_chatbot(self):
        file_path = 'templates/dataSettingWindow/TF/intentsUVG.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            chatbot_details = json.load(json_file)
        tag = self.ids.tag.text
        patterns_raw = self.ids.patterns.text
        responses_raw = self.ids.responses.text
        patterns = patterns_raw.split(",\n")
        responses = responses_raw.split(",\n")
        patterns.pop()
        responses.pop()
        new_data = {"tag": tag,
                    "patterns": patterns,
                    "responses": responses
                    }
        with open(file_path, 'r+', encoding='utf-8') as json_file:
            chatbot_details = json.load(json_file)
            chatbot_details["intents"].append(new_data)
            json_file.seek(0)
            json.dump(chatbot_details, json_file, indent=4, ensure_ascii=False)
        # Trainer.runTraining()
        self.dismiss()


# ventana para controlar max/min servo y modificar base datos chatbot
class MotorDataSettingWindow(Screen):
    def on_pre_enter(self):
        file_path = 'templates/dataSettingWindow/servos_data.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            servos_list = json.load(json_file)
        for servo in servos_list:
            id = "min_max_servo" + servo["id"]
            self.ids[str(id)].min_val = str(servo["min"])
            self.ids[str(id)].max_val = str(servo["max"])

    def guardar_min_max(self):
        file_path = 'templates/dataSettingWindow/servos_data.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            servos_list = json.load(json_file)
            for i in range(19):
                id = "min_max_servo" + str(i)
                servos_list[i]["min"] = int(self.ids[str(id)].min_val)
                servos_list[i]["max"] = int(self.ids[str(id)].max_val)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(servos_list, json_file, indent=2)

    def chatbot_data(self):
        global chatbot_details
        file_path = 'templates/dataSettingWindow/TF/intentsUVG.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            chatbot_details = json.load(json_file)
        values = []
        for intent in chatbot_details["intents"]:
            values.append(intent["tag"])
        return values

    def intent_select(self, value):
        global chatbot_details, intent_old
        pattern_value = ""
        response_value = ""
        pre_pattern_value = self.ids.patterns.text
        pre_response_value = self.ids.responses.text
        if (pre_pattern_value != "") and (pre_response_value != ""):
            for intent in chatbot_details["intents"]:
                if (intent_old == intent["tag"]):
                    pattern_array = pre_pattern_value.split(",\n")
                    response_array = pre_response_value.split(",\n")
                    pattern_array.pop()
                    response_array.pop()
                    intent["patterns"] = pattern_array
                    intent["responses"] = response_array
        intent_old = value
        for intent in chatbot_details["intents"]:
            if (value == intent["tag"]):
                for pattern in intent["patterns"]:
                    pattern_value = pattern_value + pattern + ",\n"
                for response in intent["responses"]:
                    response_value = response_value + response + ",\n"
                self.ids.patterns.text = pattern_value
                self.ids.responses.text = response_value
    
    def respuestas_detector_emociones(self, value):
        global emotion_responses
        file_path = 'templates/mainWindow/emotion_detector/respuestas.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            emotion_responses = json.load(json_file)
        responses = ""
        for emotion in emotion_responses["emotions"]:
            if (value == emotion["tag"]):
                for respuesta in emotion["responses"]:
                    responses = responses + respuesta + ",\n"
                self.ids.respuestas_emociones.text = responses

    def modificar_chatbot(self):
        global chatbot_details
        file_path = 'templates/dataSettingWindow/TF/intentsUVG.json'
        intent_select = self.ids.intent_select.text
        pattern_value = self.ids.patterns.text
        response_value = self.ids.responses.text
        pattern_array = pattern_value.split(",\n")
        response_array = response_value.split(",\n")
        pattern_array.pop()
        response_array.pop()
        for intent in chatbot_details["intents"]:
            if (intent_select == intent["tag"]):
                intent["patterns"] = pattern_array
                intent["responses"] = response_array
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(chatbot_details, json_file, ensure_ascii=False, indent=4)
        # Trainer.runTraining()
    
    def modificar_emotion_detector(self):
        global emotion_responses
        file_path = 'templates/mainWindow/emotion_detector/respuestas.json'
        emotion_selected = self.ids.emociones_selection.text
        response_value = self.ids.respuestas_emociones.text
        response_array = response_value.split(",\n")
        response_array.pop()
        for emotion in emotion_responses["emotions"]:
            if emotion_selected == emotion["tag"]:
                emotion["responses"] = response_array
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(emotion_responses,
                      json_file,
                      ensure_ascii=False,
                      indent=4)


# Inicializacion del hilo secundario
t1 = Thread(target=MainWindow().chat_bot_do)
t1.start()
t2 = Thread(target=MainWindow().chat_bot_talk)
t2.start()
t3 = Thread(target=MainWindow().emotion_detection)
t3.start()


# aplicación
class RostroAnimatronico(App):
    def build(self):
        return WindowManager()


if __name__ == '__main__':
    Config.set('kivy', 'log_dir', 'your_chosen_log_dir_path')
    Config.set('kivy', 'log_name', "anything_you_want_%y-%m-%d_%_.log")
    Config.set('kivy', 'log_maxfiles', 1000)
    Config.set('kivy', 'log_level', 'error')
    Config.write()
    RostroAnimatronico().run()
