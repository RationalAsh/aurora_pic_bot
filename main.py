#!/usr/bin/python3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging as lg

TOKEN = '236423438:AAH_98YQwozj62kufw1z2sON3vtHjR_TYK0'

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello sexy, I love Aurora,  and hence you! I'll send you beautiful pictures of yourself whenever you need me to :wink:")

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
