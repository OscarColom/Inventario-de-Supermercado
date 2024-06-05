from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivymd.uix.list import OneLineListItem  # Importa OneLineListItem
import json  
import urllib.request
import openai
import os

Window.size = (350, 500)

# Definimos los nombres de los archivos JSON
USERS_FILE = 'users.json'
STOCK_FILE = 'stock.json'

class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class WelcomeScreen(Screen):
    pass

class AddStockScreen(Screen):
    pass

class ViewStockScreen(Screen):
    pass

class MyApp(MDApp):

    def build(self):
        self.title = "Inventario de Supermercado"
        return Builder.load_file('main.kv')

    def on_start(self):
        self.load_users()
        self.load_stock()

    def load_users(self):
        try:
            with open(USERS_FILE, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}

    def save_users(self):
        with open(USERS_FILE, 'w') as f:
            json.dump(self.users, f)

    def load_stock(self):
        try:
            with open(STOCK_FILE, 'r') as f:
                self.stock = json.load(f)
        except FileNotFoundError:
            self.stock = {}

    def save_stock(self):
        with open(STOCK_FILE, 'w') as f:
            json.dump(self.stock, f)

    def register(self, username, password, confirm_password):
        if not username or not password or not confirm_password:
            self.show_snackbar("Por favor, completa todos los campos")
            return

        if password != confirm_password:
            self.show_snackbar("Las contraseñas no coinciden")
            return

        if username in self.users:
            self.show_snackbar("El nombre de usuario ya existe")
            return

        self.users[username] = password
        self.save_users()
        self.root.current = 'login'
        self.show_snackbar("Usuario registrado con éxito")

    def login(self, username, password):
        if not username or not password:
            self.show_snackbar("Por favor, completa todos los campos")
            return

        if username not in self.users or self.users[username] != password:
            self.show_snackbar("Credenciales incorrectas")
            return

        self.root.current = 'welcome'
        self.show_snackbar(f"Bienvenido, {username}")

    def logout(self):
        self.root.current = 'login'
        self.show_snackbar("Sesión cerrada")

    def add_stock(self, item_name, item_quantity):
        if not item_name or not item_quantity:
            self.show_snackbar("Por favor, completa todos los campos")
            return

        if item_name in self.stock:
            self.stock[item_name] += int(item_quantity)
        else:
            self.stock[item_name] = int(item_quantity)

        self.save_stock()
        self.root.current = 'welcome'
        self.show_snackbar(f"Stock añadido: {item_name} - {item_quantity}")

    def view_stock(self):
        stock_list = self.root.get_screen('view_stock').ids.stock_list
        stock_list.clear_widgets()

        for item_name, item_quantity in self.stock.items():
            stock_list.add_widget(
                OneLineListItem(text=f"{item_name}: {item_quantity}")
            )

    def show_snackbar(self, text):
        snackbar = Snackbar(
            text,
            snackbar_x=dp(10),
            snackbar_y=dp(10),
            size_hint_x=(Window.width - dp(20)) / Window.width
        )
        snackbar.open()

if __name__ == '__main__':
    MyApp().run()
