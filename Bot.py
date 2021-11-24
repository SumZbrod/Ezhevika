from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
import logging
from config import *

# import PySimpleGUI as sg

max_length = 2**12

logging.basicConfig(format='%(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

updater = None

with open(token_path) as f:
    TOKEN = f.read()

def start_bot():
    global updater
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('registration', registration))
    updater.start_polling()
    updater.idle()

def start(update, context):
    start_help = '/registration'
    update.message.reply_text(start_help)

def registration(update, context):
    string = 'r'
    update.message.reply_text(string)

if __name__ == '__main__':
    start_bot()