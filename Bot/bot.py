import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import json
import datetime

# Замените на ваш реальный токен
TOKEN = '7932440241:AAFxSHJxsHHt98ONUMp8lcsJt7XVCXkEXkM'

# URL вашего веб-приложения (убедитесь, что это правильный URL Web App)
WEB_APP_URL = 'https://tiny-stroopwafel-7dbe54.netlify.app/#'


bot = telebot.TeleBot(TOKEN)

# Временное хранилище данных (в реальном приложении используйте БД)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    # Получаем имя пользователя
    first_name = message.from_user.first_name or "дорогой друг"

    # Создаем кнопку для открытия веб-приложения
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(
        text="📖 Открыть корзинку",
        web_app=WebAppInfo(WEB_APP_URL)
    )
    markup.add(btn)

    # Приветственное сообщение
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Привет, {first_name}! 🌸\n\n'
             f'Пришло время собрать свою личную корзинку для стабильной жизни и ясного разума! Готов?🛒\n\n'
             f'Тогда нажми кнопку ниже, чтобы открыть дневник',
        reply_markup=markup
    )


@bot.message_handler(content_types=['text', 'photo', 'voice'])
def handle_content(message):
    # Сохраняем контент пользователя
    user_id = message.from_user.id
    today = datetime.date.today().isoformat()

    if user_id not in user_data:
        user_data[user_id] = {}

    if today not in user_data[user_id]:
        user_data[user_id][today] = {
            'texts': [],
            'photos': [],
            'voices': []
        }

    if message.text:
        user_data[user_id][today]['texts'].append(message.text)
        bot.reply_to(message, "✅ Текст сохранен в дневнике!")
    elif message.photo:
        user_data[user_id][today]['photos'].append(message.photo[-1].file_id)
        bot.reply_to(message, "📸 Фото сохранено в дневнике!")
    elif message.voice:
        user_data[user_id][today]['voices'].append(message.voice.file_id)
        bot.reply_to(message, "🎤 Голосовое сообщение сохранено!")


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)