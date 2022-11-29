import telebot

token = "5799376078:AAHNZx94tPIRx-OszvsoN5T1OTtGS8J-SUk"

bot = telebot.Telebot(token)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    pass


# Обрабатываются все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)


