#!/usr/bin/python3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultPhoto

from keys import *
import logging as lg
import sys
from imgurpython import ImgurClient
from random import randint
from uuid import uuid4

sys.path.insert(0, '/home/telegram_bots/api_keys')

#States of the bot
BOTSTATE = 0
STARTMODE = 0
PICMODE = 1

#Inputs
NEEDPICS = 'Give me pictures :D!'
NOTHINGNOW = 'Nothing Right Now'

#Subjects
SUBJECTS = {'EARTH':'/r/earthporn',
            'SPACE': '/r/spaceporn',
            'FOOD': '/r/foodporn',
            'HISTORY': '/r/historyporn',
            'KITTENS': '/r/kittens',
            'CUTENESS': '/r/aww'}
CURRENT_SUBJECT = '/r/earthporn'
# EARTH = '/r/earthporn'
# SPACE = '/r/spaceporn'
# FOOD = '/r/foodporn'
# HISTORY = '/r/historyporn'
# KITTENS = '/r/kittens'
# CUTENESS = '/r/aww'

def start(bot, update):
    """Start off things with a welcome message and a description
    of what the bot does."""
    global BOTSTATE

    BOTSTATE = STARTMODE

    welcome_text = 'Hello Aurora! I\'m a bot that find and sends '+\
                   'you beautiful pictures of earth and space! Ashwin made '+\
                   'me as a gift to you because he knows how much '+\
                   'you love the stars and earth and because he loves you a lot!'+\
                   ' Have fun!\n\n' + \
                   'If you want to change the subject of the pictures use the command: \n'+\
                   '/subject'+\
                   telegram.emoji.Emoji.SMILING_FACE_WITH_SMILING_EYES +\
                   '\n\n What do you want to do?'
    
    custom_keyboard = [[telegram.KeyboardButton(NEEDPICS)],
                       [telegram.KeyboardButton(NOTHINGNOW)]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keybaord=True,
                                                one_time_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat_id, text=welcome_text, reply_markup=reply_markup)

def subject(bot, update):
    """Set the subject of the images from the ones available."""
    help_text = 'Select which subject you want images of.'
    custom_keyboard = [[telegram.KeyboardButton(SUB)] for SUB in SUBJECTS.keys()]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=False,
                                                one_time_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat_id, text=help_text,
                    reply_markup=reply_markup)

def unknown(bot, update):
    """Handle unknown commands."""
    unknown_resp = 'I\'m not quite sure what you are trying to tell me.'+\
                   'I do not understand that command. Can you try again? '+\
                   'Send /start to get started.'
    bot.sendMessage(chat_id=update.message.chat_id, text=unknown_resp)

def state_change(bot, update):
    """Handle state changes by checking the reply from the custom keyboard."""
    global BOTSTATE
    global CURRENT_SUBJECT

    user_req = update.message.text

    bye_text = 'Okay! I\'m always here if you need pictures of aurorae! ^_^'

    unknown_resp = 'I\'m not quite sure what you are trying to tell me.'+\
                   'I do not understand that command. Can you try again? '+\
                   'Send /start to get started.'

    custom_keyboard = [[ telegram.KeyboardButton(NEEDPICS),
                         telegram.KeyboardButton(NOTHINGNOW)]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keybaord=True,
                                                one_time_keyboard=True)

    #If Aurora needs pics
    if user_req == NEEDPICS:
        BOTSTATE = PICMODE
        #Send chat action
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=telegram.ChatAction.UPLOAD_PHOTO)
        #Get a random filename
        links, titles = getImageLinks()
        #Send random recent picture
        randInd = randint(0,49)
        bot.sendPhoto(chat_id=update.message.chat_id, 
                      photo=links[randInd], caption=titles[randInd])

    elif user_req == NOTHINGNOW:
        bot.sendMessage(chat_id=update.message.chat_id, text=bye_text)
    elif user_req in SUBJECTS.keys():
        #Change the current subject to the requested one
        CURRENT_SUBJECT = SUBJECTS[user_req]
        bot.sendMessage(chat_id=update.message.chat_id, text='What do you want right now?', 
                        reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=unknown_resp)
    #print(user_req)

def get_thumb_url(url):
    """Helper function to get the thumbnail URL of an imgur image"""
    #Find the . of the extension from the end
    idx = -url[::-1].find('.') - 1
    thumb_url = url[:idx] + 'l' + url[idx:]
    return thumb_url

def inline_query(bot, update):
    """Respond to inline query with images of earth and space."""
    query = update.inline_query.query

    pagenum = 1

    #If the query is an integer, interpret as page number
    try:
        pagenum = int(query)
    except:
        pass
    
    links, titles = getImageLinks(pagenum)

    results = [InlineQueryResultPhoto(id=uuid4(), photo_url=link, 
                                      thumb_url=get_thumb_url(link),
                                      title=tit) for link, tit in zip(links, titles)]
    bot.answerInlineQuery(update.inline_query.id, results)

def pause(updater):
    """Pauses the polling of the bot for testing purposes"""
    updater.stop()

def getImageLinks(pagenum=1, max_links=50):
    #initialize client
    client = ImgurClient(imgur_client_id, imgur_client_secret)
    
    #Get items
    items = client.gallery(section=CURRENT_SUBJECT, sort='time', page=pagenum,
                           window='day', show_viral=False)

    #Get links
    links = [item.link for item in items]
    #Get image titles
    titles = [item.title for item in items]
    
    #Return list of links
    return links[:max_links], titles[:max_links]

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
    #Handle the subject command.
    dispatcher.add_handler(CommandHandler('subject', subject))

    #Handle inline queries
    dispatcher.add_handler(InlineQueryHandler(inline_query))

    #Handle unknown commands
    dispatcher.add_handler(MessageHandler([Filters.command], unknown))

    #Handle state transitions
    dispatcher.add_handler(MessageHandler([Filters.text], state_change))
    
    updater.start_polling()
