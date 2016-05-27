#!/usr/bin/python3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from keys import *
import logging as lg
import sys
from imgurpython import ImgurClient
from random import randint

sys.path.insert(0, '/home/telegram_bots/api_keys')

#States of the bot
BOTSTATE = 0
STARTMODE = 0
PICMODE = 1

#Inputs
NEEDPICS = 'Give me pictures :D!'
NOTHINGNOW = 'Nothing Right Now'

def start(bot, update):
    """Start off things with a welcome message and a description
    of what the bot does."""
    global BOTSTATE

    BOTSTATE = STARTMODE

    welcome_text = 'Hello Aurora! I\'m a bot that find and sends '+\
                   'you beautiful pictures of aurorae! Ashwin made '+\
                   'me as a gift to you because he knows how much '+\
                   'you love aurorae and because he loves you a lot!'+\
                   ' Have fun!' + \
                   telegram.emoji.Emoji.SMILING_FACE_WITH_SMILING_EYES +\
                   '\n\n What do you want to do?'
    
    custom_keyboard = [[ telegram.KeyboardButton(NEEDPICS),
                         telegram.KeyboardButton(NOTHINGNOW)]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keybaord=True,
                                                one_time_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat_id, text=welcome_text, reply_markup=reply_markup)

def unknown(bot, update):
    """Handle unknown commands."""
    unknown_resp = 'I\'m not quite sure what you are trying to tell me.'+\
                   'I do not understand that command. Can you try again? '+\
                   'Send /start to get started.'
    bot.sendMessage(chat_id=update.message.chat_id, text=unknown_resp)

def state_change(bot, update):
    """Handle state changes by checking the reply from the custom keyboard."""
    global BOTSTATE
    user_req = update.message.text

    bye_text = 'Okay! I\'m always here if you need pictures of aurorae! ^_^'

    unknown_resp = 'I\'m not quite sure what you are trying to tell me.'+\
                   'I do not understand that command. Can you try again? '+\
                   'Send /start to get started.'

    #If Aurora needs pics
    if user_req == NEEDPICS:
        BOTSTATE = PICMODE
        #Send chat action
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=telegram.ChatAction.UPLOAD_PHOTO)
        #Get a random filename
        links = getImageLinks()
        #Send random recent picture
        randInd = randint(0,49)
        bot.sendPhoto(chat_id=update.message.chat_id, 
                      photo=links[randInd])

    elif user_req == NOTHINGNOW:
        bot.sendMessage(chat_id=update.message.chat_id, text=bye_text)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=unknown_resp)
    #print(user_req)

def pause(updater):
    """Pauses the polling of the bot for testing purposes"""
    updater.stop()

def getImageLinks(max_links=50):
    #initialize client
    client = ImgurClient(imgur_client_id, imgur_client_secret)
    
    #Get items
    items = client.gallery(section='/r/earthporn', sort='newest', page=1,
                           window='day', show_viral=False)

    #Get links
    links = [item.link for item in items]
    
    #Return list of links
    return links[:max_links]

if __name__=='__main__':
    lg.basicConfig(level=lg.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #Initialize the bot
    bot = telegram.Bot(token=AURORABOT_TOKEN)
    print(bot.getMe())

    #Initialize imgur
    #imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)
    
    #initialize the updater for polling
    updater = Updater(token=AURORABOT_TOKEN)
    dispatcher = updater.dispatcher

    #Handle the start command.
    dispatcher.add_handler(CommandHandler('start', start))

    #Handle unknown commands
    dispatcher.add_handler(MessageHandler([Filters.command], unknown))

    #Handle state transitions
    dispatcher.add_handler(MessageHandler([Filters.text], state_change))
    
    updater.start_polling()
