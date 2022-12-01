import telebot

token = "5799376078:AAHNZx94tPIRx-OszvsoN5T1OTtGS8J-SUk"

bot = telebot.TeleBot(token)

keys = {
    'Американский доллар': 'USD',
    'Евро': 'EUR',
    'Казахстанский тенге': 'KZT'
}


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет, я умею конвертировать валюты.\
Введи команду в следующем формате:\
n<валюта>\
<в какю валюту необходимо перевести>\
<количество>\n Список валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


bot.polling()

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
# @bot.message_handler(commands=['start', 'help'])
# def handle_start_help(message):
#     pass
#
#
# # Обрабатываются все документы и аудиозаписи
# @bot.message_handler(content_types=['document', 'audio'])
# def handle_docs_audio(message):
#     pass
