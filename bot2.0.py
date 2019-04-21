import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
bot = telegram.Bot(token="873804634:AAFdPWVQSSc00kndarzPiFryLgHUqt7E6aM")
updater = Updater(token='873804634:AAFdPWVQSSc00kndarzPiFryLgHUqt7E6aM', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)


dispatcher.add_handler(echo_handler)
dispatcher.add_handler(start_handler)


updater.start_polling()
