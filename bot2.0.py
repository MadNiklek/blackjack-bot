import logging
import random
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
BET_AMOUNT, HIT_STAY, TYPING_CHOICE = range(3)
reply_keyboard = [['Hit'],['Stay']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

cards = [2,3,4,5,6,7,8,9,10,10,10,11]
# player_bet = 0
# dealer_cards = list()
# player_cards = list()
#


# def cards_to_str(user_data):
#     cards = list()
#     for key, value in user_data.items():
#         cards.append('{} - {}'.format(key, value))
#
#     return "\n".join(cards).join(['\n', '\n'])

def start(update, context):
    update.message.reply_text("Hi! Welcome to BlackJakc.\n"
                              "Type /help for commands list.")
def help(update, context):
    update.message.reply_text("/start - Start the bot\n"
                              "/game - Start the game\n"
                              "/cancel - Cancel the current game\n")
def game(update,context):
    global player_bet
    global dealer_cards
    global player_cards
    player_bet = 0
    dealer_cards = []
    player_cards = []
    update.message.reply_text("Insert your bet : ",reply_markup=ReplyKeyboardRemove())
    return BET_AMOUNT

def bet_amount(update,context):
    global player_bet
    global cards
    global dealer_cards
    global player_cards
    global markup
    player_bet = update.message.text
    dealer_cards.append(random.choice(cards))
    update.message.reply_text("Dealer's hand : \n? - " + str(dealer_cards[0]))
    player_cards.append(random.choice(cards))
    player_cards.append(random.choice(cards))
    update.message.reply_text("Your hand : \n" + str(player_cards) + " (" + str(sum(player_cards)) + ") Hit or stay?",reply_markup=markup )
    return HIT_STAY

def hit_choice(update,context):
    global player_bet
    global cards
    global dealer_cards
    global markup
    global player_cards
    player_cards.append(random.choice(cards))
    update.message.reply_text("Player draws " + str(player_cards[-1]))
    if sum(player_cards)>21:
        update.message.reply_text("Player has " + str(sum(player_cards)))
        update.message.reply_text("Player busted!")
        update.message.reply_text("Player loses " + str(player_bet) + " points.",reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    update.message.reply_text("Your hand : \n" + str(player_cards) + " (" + str(sum(player_cards)) +")Hit or stay?",reply_markup=markup)
    return HIT_STAY

def stay_choice(update,context):
    global player_bet
    global cards
    global dealer_cards
    global markup
    global player_cards
    # dealer draws
    while sum(dealer_cards) < 16:
        dealer_cards.append(random.choice(cards))
        update.message.reply_text("Dealer draws " + str(dealer_cards[-1]),reply_markup=ReplyKeyboardRemove())
        update.message.reply_text("Dealer has " + str(sum(dealer_cards)))
        if sum(dealer_cards) > 21:
            update.message.reply_text("Dealer busted!")
            update.message.reply_text("Player gets " + str(player_bet) + " points.")
            return ConversationHandler.END
    if sum(dealer_cards) < sum(player_cards):
        update.message.reply_text("Dealer has " + str(sum(dealer_cards)) +
                                  "\nPlayer has " + str(sum(player_cards)))
        update.message.reply_text("Player wins!")
        update.message.reply_text("Player gets " + str(player_bet) + " points.")
    elif sum(dealer_cards) > sum(player_cards):
        update.message.reply_text("Dealer has " + str(sum(dealer_cards)) +
                                  "\nPlayer has " + str(sum(player_cards)))
        update.message.reply_text("Dealer wins!")
        update.message.reply_text("Player loses " + str(player_bet) + " points.")
    elif sum(dealer_cards) == sum(player_cards):
        update.message.reply_text("Dealer has " + str(sum(dealer_cards)) +
                                  "\nPlayer has " + str(sum(player_cards)))
        update.message.reply_text("Draw!")
        update.message.reply_text("Player gets 0 points.\n:)")
    return ConversationHandler.END

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main():
    updater = Updater("873804634:AAFdPWVQSSc00kndarzPiFryLgHUqt7E6aM")
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('game', game)],

        states={
            BET_AMOUNT: [MessageHandler(Filters.text,bet_amount)],
            HIT_STAY: [MessageHandler(Filters.regex('^Hit$'),
                                    hit_choice,
                                    pass_user_data=True),
                       MessageHandler(Filters.regex('^Stay'),
                                    stay_choice),
                       ]
        },

        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
