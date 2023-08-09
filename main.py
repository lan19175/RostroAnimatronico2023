from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from pygrabber.dshow_graph import FilterGraph

Window.maximize()

Builder.load_file('templates/manager_window.kv')
Builder.load_file('templates/mainWindow/main_window.kv')
Builder.load_file('templates/dataSettingWindow/data_setting_window.kv')
Builder.load_file('templates/motorWindow/motor_window.kv')
Builder.load_file('templates/settingsWindow/settings_window.kv')


class WindowManager(ScreenManager):
    pass


class SettingWindow(Screen):
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
    def on_pre_enter(self):
        self.initial_values()

    def initial_values(self):
        for i in range(11):
            id_slider = "slider_servo" + str(i)
            id_text = "grados_servo" + str(i)
            id_angle = "servo_movible" + str(i)
            value = int(self.ids[str(id_slider)].value)
            self.ids[str(id_text)].text = f'{int(value)}°'
            self.ids[str(id_angle)].servo_angle = int(value)

    def servo_screen(self, row, col):
        pos_extra_x = col * .192
        pos_extra_y = row * .26
        window_size = Window.size
        x_pos = (pos_extra_x + .295) * window_size[0]
        y_pos = (.71 - pos_extra_y) * window_size[1]
        pos = [x_pos, y_pos]
        return pos

    def slider_func(self, no_servo, value):
        id_text = "grados_servo" + str(no_servo)
        id_angle = "servo_movible" + str(no_servo)
        self.ids[str(id_text)].text = f'{int(value)}°'
        self.ids[str(id_angle)].servo_angle = int(value)

    def initial_value(self, no_servo):
        value = [180, 50, 30, 90,
                 55, 95, 150, 10,
                 20, 160, 120, 45]
        return int(value[no_servo])


class MotorDataSettingWindow(Screen):
    pass


class AwesomeApp(App):
    def build(self):
        return WindowManager()


if __name__ == '__main__':
    AwesomeApp().run()
