import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
bot = telegram.Bot(token="873804634:AAFdPWVQSSc00kndarzPiFryLgHUqt7E6aM")
updater = Updater(token='873804634:AAFdPWVQSSc00kndarzPiFryLgHUqt7E6aM', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)

def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


unknown_handler = MessageHandler(Filters.command, unknown)
start_handler = CommandHandler('start', start)


dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(start_handler)


updater.start_polling()
