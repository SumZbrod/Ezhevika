from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, updater
import telegram
import logging
from config import *
import json
import sysconfig
import User

logging.basicConfig(format='%(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

def data2dict(raw_data):
    raw_string = str(raw_data)
    raw_string = raw_string.replace('\'', '"')
    raw_string = raw_string.replace('True', '"True"')
    raw_string = raw_string.replace('False', '"False"')
    return json.loads(raw_string)

def get_user_id(D):
    return D['message']['chat']['id']

class Tutovnik:
    def __init__(self) -> None:
        self.max_message_length = 2**12

        with open(token_path) as f:
            TOKEN = f.read()

        self.bot = telegram.Bot(token=TOKEN)
        self.updater = Updater(TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.command_dict = {
            'start': self.command_start, 
            'make_task': self.command_make_task, 
            }

        self.func_dict = {
            'make_task': self.create_task, 
            }
        

        # self.users = User.Users()

    def start_bot(self):
        for name, func in self.command_dict.items():
            self.dispatcher.add_handler(CommandHandler(name, func))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.Command_tracker))
        self.updater.start_polling()
        self.updater.idle()

    def command_start(self, update, context):
        start_help = '/make_task'
        update.message.reply_text(start_help)
    
    def Command_tracker(self, update, context):
        update_data = data2dict(update)
        user_id = get_user_id(update_data)
        if user_id in context.user_data:
            self.func_dict[context.user_data[user_id]](update, context)
            del context.user_data[user_id]

    def command_make_task(self, update, context):
        update_data = data2dict(update)
        user_id = get_user_id(update_data)
        context.user_data[user_id] = 'make_task'
    
    def create_task(self, update, context):
        text = update.message.text
        update.message.reply_text(f'task "{text}" - created')

if __name__ == '__main__':
    # send_message('hi')
    A = Tutovnik()
    A.start_bot()