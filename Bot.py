from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
import telegram
import logging
from config import *
import requests
# import PySimpleGUI as sg
logging.basicConfig(format='%(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Tutovnik:
    def __init__(self) -> None:
        self.max_message_length = 2**12

        with open(token_path) as f:
            TOKEN = f.read()

        self.bot = telegram.Bot(token=TOKEN)
        self.updater = Updater(TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.command_func_dict = {
            'start': self.start, 
            'registration': self.registration,
            'make_task': self.make_task, 
            }
        self.tracker_func_dict = {
            }

    def start_bot(self):
        for name, func in self.command_func_dict.items():
            self.dispatcher.add_handler(CommandHandler(name, func))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.command_tracker))
        self.updater.start_polling()
        self.updater.idle()

    def start(self, update, context):
        start_help = '/registration'
        update.message.reply_text(start_help)

    def registration(self, update, context):
        string = f'{update}'
        update.message.reply_text(string)
    
    def command_tracker(self, update, context):
        if context.user_data['make_task']:
            update.message.reply_text("soory, i can't now do it")

    def make_task(self, update, context):
        context.user_data['make_task'] = True

if __name__ == '__main__':
    # send_message('hi')
    A = Tutovnik()
    A.start_bot()