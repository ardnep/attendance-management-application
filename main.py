from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window

from filemanager import FileManager

Window.size = (600, 600)
Window.set_icon('window_icon.png')

LabelBase.register(name="Antipasto", fn_regular="fonts/AntipastoPro-Medium_trial.ttf", fn_bold="fonts/AntipastoPro-Extralight_trial.ttf")
LabelBase.register(name="CourierNew", fn_regular="fonts/cour.ttf")
LabelBase.register(name="Antiqua", fn_regular="fonts/BKANT.TTF")


class AttendanceApp(App):
    def build(self):
        return kv


class AppScreen(Screen):
    pass


class SecondaryScreens(AppScreen):
    pass


class AttendanceWindow(SecondaryScreens):
    pass


class TakeAttendanceWindow(SecondaryScreens):
    pass


class UpdateRecordWindow(SecondaryScreens):
    pass


class ViewRecordsWindow(SecondaryScreens):
    search_1_name = ''
    search_2_name = ''
    search_3_name = ''

    def on_enter(self, *args):
        self.search_1_name, self.search_2_name, self.search_3_name = FileManager.get_recent_searches()
        if self.search_1_name != '':
            self.ids.search_1.disabled = False
            self.ids.search_1.text = self.search_1_name
            self.ids.search_1.opacity = 1

        if self.search_2_name != '':
            self.ids.search_2.disabled = False
            self.ids.search_2.text = self.search_2_name
            self.ids.search_2.opacity = 1

        if self.search_3_name != '':
            self.ids.search_3.disabled = False
            self.ids.search_3.text = self.search_3_name
            self.ids.search_3.opacity = 1


class ViewRecordResults(Popup):

    def show_records(self, records):
        inner_content = FloatLayout()
        y = 0.85
        record_names = FileManager.return_record_names(records)
        record_buttons = {}
        delete_buttons = {}
        for index, name in enumerate(record_names):
            record_buttons.update({f'btn_{index}': Button(text=name, id=name, pos_hint={"x": 0.15, "y": y}, font_name='Antiqua')})
            delete_buttons.update({f'btn_del_{index}': Button(text='Delete', id=name, pos_hint={"x": 0.80, "y": y}, size_hint=(0.2, 0.055))})
            y -= 0.1

        for key, values in record_buttons.items():
            inner_content.add_widget(values)
            record_buttons[key].bind(on_press=FileManager.view_record)

        for key, values in delete_buttons.items():
            inner_content.add_widget(values)
            delete_buttons[key].bind(on_press=FileManager.delete_record)
            delete_buttons[key].bind(on_release=self.dismiss)

        inner_content.add_widget(Button(text='Close',
                                        pos_hint={"x": 0.80, "y": 0.02},
                                        size_hint=(0.2, 0.055),
                                        on_press=self.dismiss))
        self.content = inner_content


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("gui.kv")

if __name__ == "__main__":
    AttendanceApp().run()
