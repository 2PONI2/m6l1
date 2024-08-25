import telebot
from logic import Text2ImageAPI
from config import TOKEN, API_KEY, SECRET_KEY
from functools import wraps


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привет,я бот для генерации картинок.Что бы создать картинку используй команду /draw "запрос" .Пример запроса: /draw Вертолет на колесах')

@bot.message_handler(func=lambda message: True, commands=['draw'])
def draw(message):
    bot.send_message(message.chat.id,"Подожди, думаю...")
    prompt = message.text
    bot.send_chat_action(message.chat.id, 'typing')

    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)[0]

    file_path = 'generated_image.jpg'
    api.save_image(images, file_path)

    with open(file_path, 'rb') as photo:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_photo(message.chat.id, photo)

bot.polling()



