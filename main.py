from kivy.app import App
# from kivy.uix.widget import Widget
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
    pass


class MotorDataSettingWindow(Screen):
    pass


class AwesomeApp(App):
    def build(self):
        return WindowManager()


if __name__ == '__main__':
    AwesomeApp().run()
