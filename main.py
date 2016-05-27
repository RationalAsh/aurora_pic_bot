#!/usr/bin/python3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging as lg

TOKEN = '236423438:AAH_98YQwozj62kufw1z2sON3vtHjR_TYK0'

#States of the bot
START = 0
PIC

def start(bot, update):
    """Start off things with a welcome message and a description
    of what the bot does."""
    pratibha_id = ''
    sender_name = telegram.message.user.first_name
    welcome_text = 'Hello Aurora! I\'m a bot that find and sends'+\
                   'you beutiful pictures of aurorae! Ashwin made'+\
                   'me as a gift to you because he knows how much '+\
                   'you love aurorae! Have fun!' + \
                   telegram.emoji.Emoji.SMILING_FACE_WITH_SMILING_EYES +\
                   '\n\n What do you want to do?'
    custom_keyboard = [[ telegram.KeyboardButton('Give me pictures :D!'),
                         telegram.KeyboardButton('Nothing Right Now')]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keybaord=True,
                                                one_time_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat_id, text=welcome_text, reply_markup=reply_markup)

if __name__=='__main__':
    lg.basicConfig(level=lg.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    bot = telegram.Bot(token=TOKEN)
    print(bot.getMe())
    
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    updater.start_polling()
