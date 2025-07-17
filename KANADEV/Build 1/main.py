with open("/content/KANADEV/main.py", "w") as f:
    f.write('''
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.core.window import Window
import random, os
Window.clearcolor = (0.94, 0.94, 0.94, 1)
# Register Japanese font
if os.path.exists("NotoSansCJK-Regular.otf"):
    LabelBase.register(name="JapaneseFont", fn_regular="NotoSansCJK-Regular.otf")
    FONT = "JapaneseFont"
else:
    FONT = None
KANA = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "wo", "ん": "n"
}
class IconButton(ButtonBehavior, Image):
    pass
class KanaQuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kana_items = list(KANA.items())
        random.shuffle(self.kana_items)
        self.current_index = 0
        self.is_reverse = False
        self.results = []
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.char_label = Label(
            text="", font_size='100sp',
            color=(0, 0, 0, 1),
            font_name=FONT,
            size_hint=(1, 0.4)
        )
        self.layout.add_widget(self.char_label)
        self.grid = GridLayout(cols=3, spacing=20, size_hint=(1, 0.45), padding=[30, 0])
        self.layout.add_widget(self.grid)
        self.footer = BoxLayout(size_hint=(1, 0.1), padding=[30, 10], spacing=20)
        # Create image buttons
        home_btn = IconButton(source="HOME.png", size_hint=(None, None), size=(64, 64))
        reverse_btn = IconButton(source="REVERSE.png", size_hint=(None, None), size=(64, 64))
        retry_btn = IconButton(source="RETRY.png", size_hint=(None, None), size=(64, 64))
        reverse_btn.bind(on_press=self.toggle_reverse)
        retry_btn.bind(on_press=self.restart_quiz)
        # Add buttons with spacer between left and right
        self.footer.add_widget(home_btn)
        self.footer.add_widget(Widget())  # Spacer expands in middle
        self.footer.add_widget(reverse_btn)
        self.footer.add_widget(retry_btn)
        self.layout.add_widget(self.footer)
        self.add_widget(self.layout)
        self.generate_question()
    def generate_question(self):
        if self.current_index >= len(self.kana_items):
            self.manager.current = "results"
            return
        self.grid.clear_widgets()
        kana, romaji = self.kana_items[self.current_index]
        if self.is_reverse:
            question = romaji.upper()
            correct = kana
            all_choices = list(KANA.keys())
        else:
            question = kana
            correct = romaji.upper()
            all_choices = [r.upper() for r in KANA.values()]
        self.char_label.text = question
        wrong = random.sample([x for x in all_choices if x != correct], 5)
        choices = wrong + [correct]
        random.shuffle(choices)
        for choice in choices:
            btn = Button(
                text=choice,
                size_hint=(1, None),
                height=180,
                font_size='35sp',
                background_normal='CHOICES.png',
                background_down='CHOICES.png',
                font_name=FONT,
                color=(0, 0, 0, 1)
            )
            btn.bind(on_press=lambda x, ans=choice: self.check_answer(ans, correct, kana, romaji))
            self.grid.add_widget(btn)
    def check_answer(self, selected, correct, kana, romaji):
        is_correct = (selected.upper() == correct.upper())
        if not is_correct:
            self.results.append((kana.upper(), romaji.upper(), selected.upper()))
        self.current_index += 1
        self.generate_question()
    def toggle_reverse(self, *args):
        self.is_reverse = not self.is_reverse
        self.restart_quiz()
    def restart_quiz(self, *args):
        random.shuffle(self.kana_items)
        self.current_index = 0
        self.results = []
        self.generate_question()
class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.label = Label(
            text="Results",
            font_size='30sp',
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.label)
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.result_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.result_box.bind(minimum_height=self.result_box.setter('height'))
        self.scroll.add_widget(self.result_box)
        self.layout.add_widget(self.scroll)
        self.retry_btn = Button(text="Retry", size_hint=(1, 0.1), on_press=self.retry_quiz)
        self.layout.add_widget(self.retry_btn)
        self.add_widget(self.layout)
    def on_pre_enter(self):
        self.result_box.clear_widgets()
        quiz_screen = self.manager.get_screen("quiz")
        wrong_answers = quiz_screen.results
        if not wrong_answers:
            self.result_box.add_widget(Label(
                text="PERFECT!",
                font_size='24sp',
                font_name=FONT,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=50
            ))
        else:
            for kana, romaji, selected in wrong_answers:
                label = Label(
                    text=f"{kana} = {romaji} (You said: {selected})",
                    font_size='18sp',
                    font_name=FONT,
                    color=(0, 0, 0, 1),
                    size_hint_y=None,
                    height=40
                )
                self.result_box.add_widget(label)
    def retry_quiz(self, *args):
        self.manager.get_screen("quiz").restart_quiz()
        self.manager.current = "quiz"
class KanaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(KanaQuizScreen(name="quiz"))
        sm.add_widget(ResultScreen(name="results"))
        sm.current = "quiz"
        return sm
if __name__ == '__main__':
    KanaApp().run()
''')
