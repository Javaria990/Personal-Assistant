import os
import subprocess
import speech_recognition as sr
from datetime import datetime
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivymd.icon_definitions import md_icons
class NoteApp(MDApp):
    def build(self):
        Window.size = (800, 600)
        screen = MDScreen()
        self.note_input = MDTextField(
            multiline=True,
            hint_text="Enter your note",
            size_hint=(0.9, 0.4),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )
        screen.add_widget(self.note_input)
        voice_button = MDIconButton(
            icon="microphone",
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            theme_text_color="Custom",
            text_color=(0, 0, 128, 1),
            size_hint=(None, None),
            width="64dp",height="64dp", icon_size="48sp",
            on_release=self.take_note_voice,
        )
        screen.add_widget(voice_button)
        save_button = MDRectangleFlatButton(
            text="Save Note",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.save_note,
        )
        screen.add_widget(save_button)
        open_button = MDRectangleFlatButton(
            text="Open Note",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            on_release=self.open_note,
        )
        screen.add_widget(open_button)
        return screen
    def save_note(self, instance):
        note_text = self.note_input.text
        if note_text:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"note_{timestamp}.txt"
            file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
            with open(file_path, "w") as file:
                file.write(note_text)
            self.show_dialog("Note Saved", f"The note has been saved as '{filename}'.")
        else:
            self.show_dialog("Empty Note", "Please enter a note.")
    def open_note(self, instance):
        file_dialog = FileChooserListView()
        file_dialog.path = os.path.dirname(os.path.realpath(__file__))
        file_dialog.bind(selection=self.open_file)
        back_button = MDIconButton(
            icon="arrow-left",
            on_release=self.close_dialog,
        )
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(back_button)
        layout.add_widget(file_dialog)
        popup = Popup(
            title="Open Note",content=layout,size_hint=(0.9, 0.9),
        )
        popup.open()
    def open_file(self, instance, selection):
        if selection:
            file_path = selection[0]
            subprocess.Popen(["notepad.exe", file_path])
            self.close_dialog()
            filename = os.path.basename(file_path)
            self.show_dialog("Note Opened", f"The note '{filename}' has been opened.")
        else:
            self.show_dialog("Open Canceled", "No note has been opened.")
    def close_dialog(self, *args):
        for child in Window.children:
            if isinstance(child, Popup):
                child.dismiss()
    def take_note_voice(self, instance):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            note_text = r.recognize_google(audio)
            self.note_input.text = note_text
        except sr.UnknownValueError:
            self.show_dialog("Note Error", "Sorry, I could not understand your note.")
        except sr.RequestError:
            self.show_dialog("Note Error", "Sorry, there was an error in processing your note.")
        finally:
            self.note_input.hint_text = self.note_input.text
    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.7, 0.3),
        )
        dialog.open()
if __name__ == "__main__":
    NoteApp().run()