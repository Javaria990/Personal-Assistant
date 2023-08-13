from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import openai
with open("hidden.txt") as file:
    openai.api_key = file.read()
def get_api_response(prompt: str) -> str | None:
    text:str | None = None
    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,temperature=0.9,max_tokens=150,
            top_p=1,frequency_penalty=0,presence_penalty=0.6,stop=[' Human:', ' AI:'])
        choices: dict = response.get('choices')[0]
        text = choices.get('text')
    except Exception as e:
        print('ERROR:', e)
    return text
def update_list(message: str, pl: list[str]):
    pl.append(message)
def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt
def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)
    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'
    return bot_response
class ChatApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt_list = ['You will pretend to be a Personal Assistant dude and your name is proxy',
                            '\nHuman: What time is it?',
                            '\nAI: It is 2:22 PM Welcome!']
        self.chat_layout = None
        self.scroll_view = None
    def build(self):
        self.theme_cls.primary_palette = 'Indigo'
        layout = BoxLayout(orientation='vertical')
        self.scroll_view = ScrollView()
        layout.add_widget(self.scroll_view)
        self.chat_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.scroll_view.add_widget(self.chat_layout)
        user_input = MDTextField(hint_text="Enter message", on_text_validate=self.send_message)
        layout.add_widget(user_input)
        return layout
    def send_message(self, text_field):
        user_message = text_field.text
        text_field.text = ""
        self.display_message(user_message, True)
        bot_response = get_bot_response(user_message, self.prompt_list)
        self.display_message(bot_response, False)
    def display_message(self, message, is_user):
        message_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        if is_user:
            person = MDIconButton(
                icon="account",pos_hint = {"center_x": 0.5, "center_y": 0.55},theme_text_color = "Custom",
                text_color = (0, 0, 128, 1)
            )
            message_box.add_widget(person)
        else:
            icon = MDIconButton(
                icon="robot",pos_hint={"center_x": 0.5, "center_y": 0.50}, theme_text_color="Custom",text_color=(0, 0, 128, 1))
            message_box.add_widget(icon)
        label = MDLabel(text=message, halign="left", valign="middle", theme_text_color="Custom")
        label.text_color = [0,0,128,1]  # Navy Blue
        message_box.add_widget(label)
        self.chat_layout.add_widget(message_box)
        self.scroll_view.scroll_y = 0  # Scroll to the bottom
    def on_start(self):
        initial_message = self.prompt_list[-1][18:]
        self.display_message(initial_message, False)
if __name__ == '__main__':
    ChatApp().run()