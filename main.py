from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from pygrabber.dshow_graph import FilterGraph
import json
from kivy.properties import StringProperty, NumericProperty
# from kivy.factory import Factory

Window.maximize()

Builder.load_file('templates/manager_window.kv')
Builder.load_file('templates/mainWindow/main_window.kv')
Builder.load_file('templates/dataSettingWindow/data_setting_window.kv')
Builder.load_file('templates/motorWindow/motor_window.kv')
Builder.load_file('templates/motorWindow/emoji_window.kv')
Builder.load_file('templates/settingsWindow/settings_popup.kv')

emoji_selected = ''


class WindowManager(ScreenManager):
    pass


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
            id_slider = "slider_servo" + str(i)
            m_value = "M" + str(i+1)
            motor_window.ids[str(id_slider)].value = getattr(self,
                                                             str(m_value))


class EmojiWindow(Popup):
    def emoji_selected(self, emoji_id):
        global motor_window
        emoji_source = ('templates/motorWindow/imagenes/emojis/'
                        + emoji_id
                        + '.png')
        motor_window.ids.emoji.image_source = emoji_source
        motor_window.ids.emoji.emoji_selected = emoji_id


class SettingWindow(Popup):
    def spinner_clicked(self, value):
        pass

    def values_array(self):
        devices = FilterGraph().get_input_devices()
        available_cameras = {}
        available_cameras_label = []
        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name
            available_cameras_label.append(device_name)
        return available_cameras_label

    def conectar_com(self):
        pass


class MainWindow(Screen):
    pass


class MotorWindow(Screen):
    def send_gesto(self):
        pass

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

    def on_pre_enter(self):
        global motor_window
        motor_window = self
        self.initial_values()
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

    def initial_values(self):
        for i in range(19):
            id_slider = "slider_servo" + str(i)
            id_text = "grados_servo" + str(i)
            id_angle = "servo_movible" + str(i)
            value = int(self.ids[str(id_slider)].value)
            self.ids[str(id_text)].text = f'{int(value)}°'
            self.ids[str(id_angle)].servo_angle = int(value)

    def guardar_emoji(self):
        name_emoji = self.ids.nombre.text
        emoji_selected = self.ids.emoji.emoji_selected
        self.ids.nombre.text = ""
        motor_values = []
        for i in range(19):
            id = "slider_servo" + str(i)
            motor_values.append(int(self.ids[str(id)].value))

        new_emoji = self.new_emoji_data(name_emoji, emoji_selected,
                                        motor_values)
        with open('templates/motorWindow/emoji_data.json', 'r+') as file:
            file_data = json.load(file)
            file_data["emojis_details"].append(new_emoji)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        emoji_link_str = ('templates/motorWindow/imagenes/emojis/'
                          + emoji_selected + '.png')
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

    def servos_initial_value(self, no_servo):
        value = [180, 50, 30,
                 90, 55, 95,
                 150, 10, 20,
                 160, 120, 45,
                 70, 300, 180,
                 300, 4, 225,
                 45]
        return int(value[no_servo])

    def slider_func(self, no_servo, value):
        id_text = "grados_servo" + str(no_servo)
        id_angle = "servo_movible" + str(no_servo)
        self.ids[str(id_text)].text = f'{int(value)}°'
        self.ids[str(id_angle)].servo_angle = int(value)


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

    def on_value(self, value, min_max):
        if min_max == "min":
            self.min_val = value
        else:
            self.max_val = value

    def slider_func(self, value):
        self.servo_angle = int(value)
        self.servo_angle_text = f'{int(value)}°'


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


class AwesomeApp(App):
    def build(self):
        return WindowManager()


if __name__ == '__main__':
    AwesomeApp().run()
