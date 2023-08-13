from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDTimePicker
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime, timedelta
import os
Builder.load_file('whatever.kv')
class ScheduleItem(TwoLineAvatarIconListItem):
    time = StringProperty()
class HomeScreen(Screen):
    def show_time_picker(self):
        time_dialog=MDTimePicker()
        time_dialog.bind(time=self.set_selected_time)
        time_dialog.open()
    def set_selected_time(self, instance, time):
        time_label=self.ids.time_label
        selected_time=datetime.combine(datetime.today().date(), time)
        time_label.text=f"Selected Time: {selected_time.strftime('%I:%M %p')}"
    def switch_to_new_schedule_screen(self):
        self.manager.current = "new_schedule_screen"
    def on_enter(self):
        schedule_scroll=self.ids.schedule_scroll
        schedule_list=self.ids.schedule_list
        schedule_list.clear_widgets()
        filename=datetime.today().strftime("%Y-%m-%d") + ".txt"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                schedule_data = file.readlines()
                for data in schedule_data:
                    data=data.strip()
                    if "," in data:
                        title, time = data.split(",", 1)
                        item = ScheduleItem(text=title, secondary_text=time)
                        schedule_list.add_widget(item)
class NewScheduleScreen(Screen):
    def show_time_picker(self):
        time_dialog=MDTimePicker()
        time_dialog.bind(time=self.set_selected_time)
        time_dialog.open()
    def set_selected_time(self, instance, time):
        time_label=self.ids.time_label
        selected_time=datetime.combine(datetime.today().date(), time)
        time_label.text=f"Selected Time: {selected_time.strftime('%I:%M %p')}"
    def save_schedule_data(self):
        title_field=self.ids.title_field
        time_label=self.ids.time_label
        title=title_field.text
        selected_time=time_label.text.replace("Selected Time: ", "")
        filename=datetime.today().strftime("%Y-%m-%d") + ".txt"
        with open(filename, "a") as file:
            file.write(f"{title},{selected_time}\n")
        title_field.text = "";time_label.text = "Selected Time:"
        self.manager.current = "home_screen"
class DailySchedueleApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        screen_manager=ScreenManager()
        screen_manager.add_widget(HomeScreen(name="home_screen"))
        screen_manager.add_widget(NewScheduleScreen(name="new_schedule_screen"))
        today=datetime.today().date()
        filename=today.strftime("%Y-%m-%d") + ".txt"
        if os.path.exists(filename):
            created_date=datetime.fromtimestamp(os.path.getctime(filename)).date()
            if created_date != today:
                os.remove(filename)
        return screen_manager
if __name__ == "__main__":
    DailySchedueleApp().run()