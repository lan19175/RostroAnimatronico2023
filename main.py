from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
# from pygrabber.dshow_graph import FilterGraph
from kivy.properties import StringProperty, NumericProperty
import json
import Trainer
# from kivy.factory import Factory

# resolución aplicacion
Window.maximize()

# carga de archivos .kv
Builder.load_file('templates/manager_window.kv')
Builder.load_file('templates/mainWindow/main_window.kv')
Builder.load_file('templates/dataSettingWindow/data_setting_window.kv')
Builder.load_file('templates/motorWindow/motor_window.kv')
Builder.load_file('templates/motorWindow/emoji_window.kv')
Builder.load_file('templates/settingsWindow/settings_popup.kv')


class WindowManager(ScreenManager):
    pass


# gestos guardados en MotorWindow
class EmojiOptions(Button):
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
        pass

    def values_array(self):
        """devices = FilterGraph().get_input_devices()
        available_cameras = {}
        available_cameras_label = []
        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name
            available_cameras_label.append(device_name)"""
        available_cameras_label = ["Logitec", "Prueba 1", "internal"]
        return available_cameras_label

    def conectar_com(self):
        pass


# ventana principal
class MainWindow(Screen):
    pass


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
                text=emoji["nombre"],
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
                text=name_emoji,
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
        global chatbot_details
        pattern_value = ""
        response_value = ""
        for intent in chatbot_details["intents"]:
            if (value == intent["tag"]):
                for pattern in intent["patterns"]:
                    pattern_value = pattern_value + pattern + ",\n"
                for response in intent["responses"]:
                    response_value = response_value + response + ",\n"
                self.ids.patterns.text = pattern_value
                self.ids.responses.text = response_value

    def modificar_chatbot(self):
        file_path = 'templates/dataSettingWindow/TF/intentsUVG.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            chatbot_details = json.load(json_file)
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
        Trainer.runTraining()


# aplicación
class RostroAnimatronico(App):
    def build(self):
        return WindowManager()


if __name__ == '__main__':
    RostroAnimatronico().run()
