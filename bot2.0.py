import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import requests
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Kiev','us&appid=6615c7ed8550b538ed7b2d68919039e9')
json_object = r.json()
mainn = json_object["weather"][0]["main"]
descriptionn = json_object["weather"][0]["description"]

update_id = None


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('873804634:AAFdPWVQSSc00kndarzPiFryLgHUqt7E6aM')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None
    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message.text == "/weather":
            update.message.reply_text("Now is " + mainn + ", to be more precise it's " + descriptionn)


if __name__ == '__main__':
    main()
