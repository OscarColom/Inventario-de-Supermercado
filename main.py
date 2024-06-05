import threading
import telebot
import json
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivymd.uix.list import OneLineListItem
from functools import partial

Window.size = (350, 500)

# Definimos los nombres de los archivos JSON
USERS_FILE = 'users.json'
STOCK_FILE = 'stock.json'

# Telegram bot token
TELEGRAM_BOT_TOKEN = '7223540096:AAEFZvr_UypvTA8UlgFT4vhA7TVBZDBmn5c'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

class TelegramNotifier(threading.Thread):
    def __init__(self):
        super(TelegramNotifier, self).__init__()
        self.daemon = True  # Set the thread as daemon

    def run(self):
        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            chat_id = message.chat.id
            bot.reply_to(message, f"Hello! Your chat ID is {chat_id}")

        bot.polling()


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

class NotificationManagementScreen(Screen):
    pass

class RemoveStockScreen(Screen):
    pass

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show_snackbar_flag = True  # Flag to control Snackbar display

    def build(self):
        self.title = "Inventario de Supermercado"
        return Builder.load_file('main.kv')

    def on_start(self):
        self.load_users()
        self.load_stock()
        # Start the Telegram notifier thread
        notifier_thread = TelegramNotifier()
        notifier_thread.start()

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
        self.show_snackbar_flag = False  # Suppress Snackbar
        self.show_snackbar(f"Bienvenido, {username}")

    def logout(self):
        self.root.current = 'login'
        self.show_snackbar_flag = False  # Suppress Snackbar
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
        self.show_snackbar_flag = False  # Suppress Snackbar
        self.show_snackbar(f"Stock añadido: {item_name} - {item_quantity}")

    def view_stock(self):
        stock_list = self.root.get_screen('view_stock').ids.stock_list
        stock_list.clear_widgets()

        for item_name, item_quantity in self.stock.items():
            stock_list.add_widget(
                OneLineListItem(text=f"{item_name}: {item_quantity}")
            )

    def send_id(self):
        # This method is now running on a separate thread, no changes needed.
        pass

    def send_notification(self):
        chat_id = self.root.get_screen('notification_management').ids.chat_id.text

        if not chat_id:
            self.show_snackbar("Por favor, ingrese el ID del chat")
            return

        stock_message = "Current stock:\n"
        for item_name, item_quantity in self.stock.items():
            stock_message += f"{item_name}: {item_quantity}\n"

        bot.send_message(chat_id, stock_message)
        self.show_snackbar("Notificación enviada con éxito")

    def show_snackbar(self, text):
        if self.show_snackbar_flag:
            snackbar = Snackbar(
                text,
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=(Window.width - dp(20)) / Window.width
            )
            snackbar.open()

    def show_remove_stock(self):
        self.update_remove_stock_list()

    def update_remove_stock_list(self):
        screen = self.root.get_screen('remove_stock')
        stock_list = screen.ids.stock_list
        stock_list.clear_widgets()

        for item_name, item_quantity in self.stock.items():
            stock_list.add_widget(
                OneLineListItem(text=f"{item_name}: {item_quantity}", on_release=partial(self.remove_stock_item, item_name))
            )

    def remove_stock_item(self, item_name, *args):
        if item_name in self.stock:
            self.stock[item_name] -= 1
            if self.stock[item_name] <= 0:
                del self.stock[item_name]
            self.save_stock()
            self.update_remove_stock_list()
            self.show_snackbar(f"Se ha restado 1 unidad de {item_name}. Nuevo stock: {self.stock.get(item_name, 0)}")
        else:
            self.show_snackbar("Error: El elemento no existe en el stock")

if __name__ == '__main__':
    MyApp().run()
