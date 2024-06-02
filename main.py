from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.snackbar import Snackbar
import json  
import urllib.request
import openai
import os


Window.size = (350, 500)

class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class WelcomeScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"

        Builder.load_file('main.kv')

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(RegisterScreen(name="register"))
        self.screen_manager.add_widget(WelcomeScreen(name="welcome"))

        return self.screen_manager

    def load_users(self):
        if not os.path.exists('users.json'):
            with open('users.json', 'w') as f:
                json.dump({}, f)

        with open('users.json', 'r') as f:
            return json.load(f)

    def save_users(self, users):
        with open('users.json', 'w') as f:
            json.dump(users, f)

    def register(self, username, password, confirm_password):
        if not username or not password or not confirm_password:
            self.show_snackbar("Por favor, completa todos los campos")
            return

        if password != confirm_password:
            self.show_snackbar("Las contraseñas no coinciden")
            return

        users = self.load_users()
        if username in users:
            self.show_snackbar("El nombre de usuario ya existe")
            return

        users[username] = password
        self.save_users(users)
        self.show_snackbar("Usuario registrado exitosamente")
        self.root.current = "login"

    def login(self, username, password):
        if not username or not password:
            self.show_snackbar("Por favor, completa todos los campos")
            return

        users = self.load_users()
        if username not in users:
            self.show_snackbar("Nombre de usuario incorrecto")
            return

        if users[username] != password:
            self.show_snackbar("Contraseña incorrecta")
            return

        self.root.current = "welcome"
        self.show_snackbar(f"Bienvenido, {username}")


    def show_snackbar(self, snackbar_text):
        Snackbar(snackbar_text).open()

if __name__ == "__main__":
    MyApp().run()
