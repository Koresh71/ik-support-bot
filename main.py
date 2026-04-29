from flask import Flask, request
import telebot
import os

# Твои данные
TOKEN = '7827491375:AAHLDJ2jdOoYnQ4pUeYmqtX7yRiaVgMDU1o'
ADMIN_ID = 1260117006

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # URL подставится после деплоя на Vercel
    return "Бот IK Designs активен", 200

# Логика бота
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "💠 IK Designs | Автономный ассистент запущен.")

@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    if message.from_user.id != ADMIN_ID:
        user_info = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        bot.send_message(ADMIN_ID, f"📩 Новое обращение:\nОт: {user_info}\nТекст: {message.text}")
        bot.reply_to(message, "✅ Запрос передан специалисту.")