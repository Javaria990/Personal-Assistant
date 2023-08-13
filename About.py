from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout

class PersonalAssistantApp(MDApp):
    def build(self):
        sm = ScreenManager()
        screen = Screen()
        layout = BoxLayout(orientation='vertical', spacing=1, padding=(1, 5))
        title = MDLabel(
            text="[size=50][b][u]Personal Assistant[/u][/b][/size]",
            halign="center",
            markup=True,
            font_style="H4",
            theme_text_color="Custom",
            text_color=(0, 0, 0.5, 1)
        )
        line1 = MDLabel(
            text='''[size=20]This is the project named [color=#800080]Personal Assistant[/color] made by [color=#800080]Javaria Ahmad[/color] under the course of [color=#800080]Programming Fundamentals and Data Science[/color] in the year [color=#800080]2023[/color]
            The project aims to provide an assistant to the user that is able to show schedules, set reminders, take notes from the user, and provide information just like a [color=#800080]Chat-GPT[/color].
            While clicking on the different buttons, the user can perform all these tasks on the same platform. The project is made by using Python and Kivymd, and it provides a more attractive and appealing interface to the users to perform all the above-mentioned tasks...
                 For any query you can mail us at [color=#0000FF][u]javariaahmed2004@gmail.com[/u][/color][/size]''',
            halign="center",
            markup=True,
            theme_text_color="Custom",
            text_color= (0.275, 0.51, 0.706, 1)
        )
        layout.add_widget(title)
        layout.add_widget(line1)
        screen.add_widget(layout)
        sm.add_widget(screen)
        return sm
if __name__ == "__main__":
    PersonalAssistantApp().run()