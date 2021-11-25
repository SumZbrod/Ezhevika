import os
import pandas as pd

cwd = os.getcwd() + '/'

path_to_data = cwd + 'data/'
path_to_users = path_to_data + 'users.csv'

random_id = (10**6, 10**7)

def_feature = {
    'skills': {
        'max_count_of_task': 2,
        'max_days_for_task': 2,
        'max_stamina': 100,
    },
    'stata': {
        'level': 0,
        'xp': 0,
        'stamina': 100,
    }
}

#Tasklist

statuses_for_task = ['plan', 'performed', 'drop', 'done']

def_tasklist = {
    'name': [],
    'day_for': [],
    'dead_line': [],
    'status': [],
}



def_user = {
        'user_id' : None,
        'level': 0,
        'xp': 0,
        'stamina': 100,
        'max_count_of_task': 2,
        'max_days_for_task': 2,
        'max_stamina': 100,
        'number_of_tasks': 0
}

users_columns = list(def_user.keys())

if not os.path.exists(path_to_users):
    pd.DataFrame(columns=users_columns).to_csv(path_to_users, index=False)

#BOT

token_path = 'TOKEN'