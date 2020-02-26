import threading
import telebot
import time
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from hashlib import sha256

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Bot(object, metaclass=Singleton):

    def __init__(self):
        token = "<bot_token>"
        self.bot = telebot.TeleBot(token)
        self.salt = "<some_salt_string>"

        self.bs = AES.block_size
        self.key = hashlib.sha256(self.salt.encode()).digest()

        t = threading.Thread(target=self.StartBot)
        t.daemon = True
        t.start()

    def StartBot(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            chatId = message.chat.id
            token = self.encrypt(str(message.chat.id))
            self.bot.send_message(message.chat.id, "Держи токен: "+str(token, "utf-8"))

        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
        	self.bot.reply_to(message, message.text)

        self.bot.polling()

    def SendMessage(self,token, message):
        chatId = int(self.decrypt(token))
        self.bot.send_message(chatId, message)


    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
