from const import token
import telebot
from telebot import types

bot = telebot.TeleBot(token)

markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard = True)
itembtn1 = types.KeyboardButton('/binarysearch')
markup.add(itembtn1)


@bot.message_handler(commands=["binarysearch"])
def asdsad(message):
    bot.reply_to(message,message.chat.id)

@bot.message_handler(commands=["alg"])
def on_ping(message):
    bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)



@bot.message_handler(commands=["remove"])
def remove(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.send_message(message.chat.id,"thx" , reply_markup=markup)









if __name__ == '__main__':
	bot.polling(none_stop=True)
	