from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from pygrabber.dshow_graph import FilterGraph
import json
# from kivy.factory import Factory

Window.maximize()

Builder.load_file('templates/manager_window.kv')
Builder.load_file('templates/mainWindow/main_window.kv')
Builder.load_file('templates/dataSettingWindow/data_setting_window.kv')
Builder.load_file('templates/motorWindow/motor_window.kv')
Builder.load_file('templates/motorWindow/emoji_window.kv')
Builder.load_file('templates/settingsWindow/settings_popup.kv')

emoji_link = ''
emoji_selected = ''
"""emoji_json = open('templates/motorWindow/emoji_data.json')
data = json.load(emoji_json)
for i in data['emojis_details']:
    print(i)"""


class WindowManager(ScreenManager):
    pass


class EmojiOptions(Button):
    pass


class EmojiWindow(Popup):
    def emoji_selected(self, emoji_id):
        global emoji_link, emoji_selected
        emoji_source = ('templates/motorWindow/imagenes/emojis/'
                        + emoji_id
                        + '.png')
        emoji_link = emoji_source
        emoji_selected = emoji_id


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
    def new_emoji_data(self, name, emoji, motores):
        jsnon_string = {
            "nombre": name,
            "emoji": emoji,
            "M1": motores[0],
            "M2": motores[1],
            "M3": motores[2],
            "M4": motores[3],
            "M5": motores[4],
            "M6": motores[5],
            "M7": motores[6],
            "M8": motores[7],
            "M9": motores[8],
            "M10": motores[9],
            "M11": motores[10],
            "M12": motores[11],
            "M13": motores[12],
            "M14": motores[13],
            "M15": motores[14],
            "M16": motores[15],
            "M17": motores[16],
            "M18": motores[17],
            "M19": motores[18]
        }
        return jsnon_string

    def on_pre_enter(self):
        self.initial_values()

    def initial_values(self):
        for i in range(19):
            id_slider = "slider_servo" + str(i)
            id_text = "grados_servo" + str(i)
            id_angle = "servo_movible" + str(i)
            value = int(self.ids[str(id_slider)].value)
            self.ids[str(id_text)].text = f'{int(value)}°'
            self.ids[str(id_angle)].servo_angle = int(value)

    def guardar_emoji(self):
        global emoji_link, emoji_selected
        name_emoji = self.ids.nombre.text
        self.ids.nombre.text = ""
        motor_values = []
        for i in range(19):
            id = "slider_servo" + str(i)
            motor_values.append(str(self.ids[str(id)].value))

        new_emoji = self.new_emoji_data(name_emoji, emoji_selected,
                                        motor_values)
        with open('templates/motorWindow/emoji_data.json', 'r+') as file:
            file_data = json.load(file)
            file_data["emojis_details"].append(new_emoji)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        
        new = EmojiOptions(text=name_emoji)
        self.ids.emoji_options.add_widget(new)

    def menu_pos(self):
        window_size = Window.size
        x_pos = window_size[0] - 250
        y_pos = 15
        pos = [x_pos, y_pos]
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


class MotorDataSettingWindow(Screen):
    pass


class AwesomeApp(App):
    def build(self):
        return WindowManager()


if __name__ == '__main__':
    AwesomeApp().run()
