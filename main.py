from kivy.app import App
# from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from pygrabber.dshow_graph import FilterGraph
Window.maximize()


class SettingWindow(Screen):
    def spinner_clicked(self, value):
        self.ids.click_label.text = f'You selected: {value}'

    def values_array(self):
        devices = FilterGraph().get_input_devices()
        available_cameras = {}
        available_cameras_label = []
        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name
            available_cameras_label.append(device_name)

        return available_cameras_label


class MainWindow(Screen):
    pass


class MotorWindow(Screen):
    pass


class MotorDataSettingWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('templates/screens.kv')


class AwesomeApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    AwesomeApp().run()
