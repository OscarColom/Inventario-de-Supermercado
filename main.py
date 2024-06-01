from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.snackbar import Snackbar
import urllib.request
import openai
import os

Window.size = (350, 500)

class WelcomeScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(WelcomeScreen(name="welcome"))

        return self.screen_manager

    def show_snackbar(self, text):
        Snackbar(text=text).open()

if __name__ == "__main__":
    MyApp().run()
