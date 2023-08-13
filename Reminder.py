from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.button import MDFlatButton
from kivy.uix.label import Label
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import platform
import subprocess
import winsound
if platform.system() == 'Windows':
    from win10toast import ToastNotifier
KV = '''
ScreenManager:
    MainScreen:
    AddReminderScreen:
<MainScreen>:
    name: 'main_screen'
    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            MDList:
                id: reminder_list
        MDIconButton:
            icon: 'plus'
            pos_hint: {'center_x': 0.5}
            on_release: app.root.current = 'add_reminder_screen'
            md_bg_color: app.theme_cls.primary_color
<AddReminderScreen>:
    name: 'add_reminder_screen'
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'
        MDTextField:
            id: reminder_title_input
            hint_text: "Reminder Title"
            mode: "fill"
            required: True
        MDTextField:
            id: reminder_text_input
            hint_text: "Reminder Text"
            mode: "fill"
            required: True
        MDTextField:
            id: reminder_date_input
            hint_text: "Date (YYYY-MM-DD)"
            mode: "fill"
            required: True
            on_focus: if self.focus: app.show_date_picker()
        MDTextField:
            id: reminder_time_input
            hint_text: "Time (HH:MM)"
            mode: "fill"
            required: True
            on_focus: if self.focus: app.show_time_picker()
        MDIconButton:
            icon: 'check'
            pos_hint: {'center_x': 0.5}
            on_release: app.add_reminder(reminder_title_input.text, reminder_text_input.text, reminder_date_input.text, reminder_time_input.text)
'''
class MainScreen(MDScreen):
    pass
class AddReminderScreen(MDScreen):
    pass
class ReminderBuilderApp(MDApp):
    reminder = None
    scheduler = BackgroundScheduler()
    def build(self):
        self.screen_manager = Builder.load_string(KV)
        self.reminder_list = self.screen_manager.get_screen('main_screen').ids.reminder_list
        return self.screen_manager
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.set_date)
        date_dialog.open()
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.set_time)
        time_dialog.open()
    def set_date(self, instance, value, date_range):
        add_reminder_screen = self.screen_manager.get_screen('add_reminder_screen')
        add_reminder_screen.ids.reminder_date_input.text = value.strftime('%Y-%m-%d')
    def set_time(self, instance, value):
        add_reminder_screen = self.screen_manager.get_screen('add_reminder_screen')
        add_reminder_screen.ids.reminder_time_input.text = value.strftime('%H:%M')
    def add_reminder(self, title, message, date_str, time_str):
        try:
            reminder_datetime=datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
            current_datetime = datetime.now()
            time_difference=reminder_datetime - current_datetime
            seconds_until_reminder = time_difference.total_seconds()
            if seconds_until_reminder <= 0:
                print("Reminder time should be in the future.")
                return
            if self.reminder:
                print("Only one reminder can be set at a time.")
                return
            self.reminder = (title, message, reminder_datetime)
            self.update_reminder_list()
            self.show_save_message()
            self.screen_manager.current = 'main_screen'
            self.scheduler.add_job(self.notify_and_beep, 'date', run_date=reminder_datetime,
                                   args=[title, message])
            self.scheduler.start()
            print("Reminder saved and set.")
        except ValueError:
            print("Invalid date or time format")
    def notify_and_beep(self, title, message):
        self.show_notification(title, message)
        self.sound_beep()
    def show_save_message(self):
        dialog = MDDialog(
            title="Reminder Saved",
            text="Your reminder has been saved.",
            buttons=[
                MDFlatButton(
                    text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()
    def show_notification(self, title, message):
        winsound.Beep(2000, 2000)
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=10)
    def update_reminder_list(self):
        self.reminder_list.clear_widgets()
        if self.reminder:
            title, message, reminder_datetime = self.reminder
            item = TwoLineListItem(text=title, secondary_text=message)
            self.reminder_list.add_widget(item)
        else:
            self.reminder_list.add_widget(Label(text="No reminder set"))
    def on_stop(self):
        self.scheduler.shutdown()
    def on_start(self):
        self.screen_manager.current = 'main_screen'
ReminderBuilderApp().run()