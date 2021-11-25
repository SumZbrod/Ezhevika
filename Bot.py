from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, updater
import telegram
import logging
from config import *
import json
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

def get_user_id(raw_data):
    D = data2dict(raw_data)
    return D['message']['chat']['id']

def get_user_name(raw_data):
    D = data2dict(raw_data)
    return D['message']['chat']['first_name']


class Tutovnik:
    def __init__(self) -> None:
        # self.max_message_length = 2**12

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
            'create_task_name': self.create_task_name, 
            }
        self.Users = User.Users()

    def start_bot(self):
        for name, func in self.command_dict.items():
            self.dispatcher.add_handler(CommandHandler(name, func))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.Command_tracker))
        self.updater.start_polling()
        self.updater.idle()

    def command_start(self, update, context):
        start_help = '/make_task'
        user_id = get_user_id(update)
        name = get_user_name(update)
        update.message.reply_text(f'Welcome {name}!')
        self.Users.user_check(user_id)
    
    def Command_tracker(self, update, context):
        user_id = get_user_id(update)

        if user_id not in context.user_data:
            self.command_start(update, context)

        elif context.user_data[user_id]:
            self.func_dict[context.user_data[user_id]](update, context)
            context.user_data[user_id] = False

    def command_make_task(self, update, context):
        user_id = get_user_id(update)
        if self.users.able_to_task(user_id):
            update.message.reply_text('Enter the name of your task')
            context.user_data[user_id] = 'create_task_name'
        else:
            update.message.reply_text("Sorry, you don't have enogth stamina for add another task")
            update.message.reply_text("If you want more stamina you need to level up, read more in /help")

    def create_task_name(self, update, context):
        text = update.message.text
        update.message.reply_text(f'task "{text}" - created!')

if __name__ == '__main__':
    # send_message('hi')
    A = Tutovnik()
    A.start_bot()