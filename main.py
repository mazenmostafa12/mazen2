import telebot


bot = telebot.TeleBot("6573362642:AAGCVTLV2z-bJx0m79ufQCiF6v2_ow1MXqU")


@bot.message_handler()
def Myfunc(message):
    bot.send_message(message.chat.id, "Hi, What's happend?")


bot.infinity_polling(skip_pending=True)
