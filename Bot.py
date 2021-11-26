from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, updater
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telebot import types 
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
    D = json.loads(raw_string)
    if 'callback_query' in D:
        D = D['callback_query']
    return D

def get_user_id(raw_data):
    D = data2dict(raw_data)

    return D['message']['chat']['id']

def get_user_name(raw_data):
    D = data2dict(raw_data)
    return D['message']['chat']['first_name']

def isnumber(x:str):
    x = x.replace('.', '')
    x = x.replace(',', '')
    return x.isnumeric()

class Tutovnik:
    def __init__(self) -> None:
        # print('\n\t __init__\n')
        # self.max_message_length = 2**12

        with open(token_path) as f:
            TOKEN = f.read()

        self.bot = telegram.Bot(token=TOKEN)
        self.updater = Updater(TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.command_dict = {
            'start': self.command_start, 
            'profile': self.command_profile,
            'make_task': self.command_make_task, 
            }

        self.func_dict = {
            'create_task_name': self.create_task_name, 
            'set_number_of_days': self.set_number_of_days,
            }
        self.Users = User.Users()

    def start_bot(self):
        # print('\n\t start_bot\n')
        for name, func in self.command_dict.items():
            self.dispatcher.add_handler(CommandHandler(name, func))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.Command_tracker))
        self.dispatcher.add_handler(CallbackQueryHandler(self.button))
        self.updater.start_polling()
        self.updater.idle()

    def button(self, update: Updater, context: CallbackContext):
        # print()
        # print(update)
        # print()
        query = update.callback_query
        query.answer()
        # query.edit_message_text(text=f"Selected option: {query.data}")
        self.command_profile(update, context)

    def command_start(self, update, context):
        # print('\n\t command_start\n')
        name = get_user_name(update)
        user_id = get_user_id(update)
        tasklist_button = telegram.InlineKeyboardButton('/profile',  callback_data="1")
        markup = telegram.InlineKeyboardMarkup([[tasklist_button]])
        # tasklist_button = types.KeyboardButton('tasklist')
        # profile_button = types.KeyboardButton('profile')
        # markup.add(tasklist_button, profile_button)
        update.message.reply_text(f'Welcome {name}!')
        update.message.reply_text(f'Try the /help',)
        self.bot.send_message(user_id, user_id, reply_markup=markup)
        self.user_check(update, context)

    def user_check(self, update, context):
        # print('\n\t user_check\n')
        user_id = get_user_id(update)
        self.Users.user_check(user_id)
        context.user_data[user_id] = {'command': None, 'data': None}
        print('~')
        print(self.Users.users_table)
        print('~')
    
    def command_profile(self, update, context):
        user_id = get_user_id(update)
        tasklist = self.Users.get_tasklist(user_id)
        profile = self.Users.get_profile(user_id)
        self.bot.send_message(user_id, f'{profile}')
        self.bot.send_message(user_id, f'{tasklist}')

    def Command_tracker(self, update, context):
        # print('\n\t Command_tracker\n')
        user_id = get_user_id(update)
        if len(context.user_data) == 0:
            self.user_check(update, context)
        elif context.user_data[user_id]['command']:
            self.func_dict[context.user_data[user_id]['command']](update, context)
        
    def command_make_task(self, update, context):
        # print('\n\t command_make_task\n')
        user_id = get_user_id(update)
        if len(context.user_data) == 0:
            self.user_check(update, context)
        if self.Users.able_to_task(user_id):
            update.message.reply_text('Enter the name of your task')
            context.user_data[user_id]['command'] = 'create_task_name'
        else:
            update.message.reply_text("Sorry, you don't have enogth stamina for add another task")
            update.message.reply_text("If you want more stamina you need to level up, read more in /help")
            context.user_data[user_id]['command'] = None

    def create_task_name(self, update, context):
        # print('\n\t create_task_name\n')
        text = update.message.text
        user_id = get_user_id(update)
        context.user_data[user_id]['data'] = {'task': {'name': text}}
        update.message.reply_text('Enter the number of days for this task')  
        context.user_data[user_id]['command'] = 'set_number_of_days'

    def set_number_of_days(self, update, context):
        # print('\n\t set_number_of_days\n')
        days = update.message.text
        user_id = get_user_id(update)
        if isnumber(days):
            days = days.replace(',', '')
            days = float(days)
            max_days_for_task = self.Users.users_table.loc[user_id]['max_days_for_task']
            if days <= max_days_for_task:
                context.user_data[user_id]['data']['task']['day_for'] = days
                self.Users.make_task(user_id, context.user_data[user_id]['data']['task'])
                update.message.reply_text("Well done!")
                context.user_data[user_id]['command'] = None
                context.user_data[user_id]['data'] = None
                self.command_profile(update, context)
            else:
                update.message.reply_text(f"Sorry, your max limit for days is {max_days_for_task}")
                update.message.reply_text("If you want more stamina you need to level up, read more in /help")
        else:
            update.message.reply_text(f"'{days}' it's not a number")
            update.message.reply_text(f"Please try again")

    def send_message(self, user_id, text):
        self.bot.send_message(user_id, text)
if __name__ == '__main__':
    # send_message('hi')
    A = Tutovnik()
    A.start_bot()
    # A.send_message(1094965520, 'реклама')