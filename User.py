from config import *
import joblib
import numpy as np
from datetime import datetime as dt 
import os
from time import time 
class Users:
    def __init__(self) -> None:
        self.users_table = pd.read_csv(path_to_users)
        self.users_table.set_index('user_id', inplace=True)

    def make_user_path(self, user_id):
        return f'{path_to_data}{user_id}/'

    def user_check(self, user_id):
        if user_id not in self.users_table.index:
            print('creatinf user')
            new_user = def_user.copy()
            new_user['user_id'] = user_id
            new_user = pd.Series(new_user)
            new_user.name = user_id
            self.users_table = self.users_table.append(new_user)
            user_path = self.make_user_path(user_id)
            if not os.path.exists(user_path):
                os.makedirs(user_path)
            pd.DataFrame(def_tasklist).to_csv(f'{user_path}tasklist.csv', index=False)
            self.save()
        else:
            print('user exists')

    def get_tasklist(self, user_id):
        user_path = self.make_user_path(user_id)
        tasklist_path = user_path+'tasklist.csv'
        tasklist = pd.read_csv(tasklist_path)
        return tasklist
    
    def get_profile(self, user_id):
        return self.users_table.loc[user_id]
    # def default_data(self, ):
    #     feature = def_feature.copy()
    #     tasklist = pd.DataFrame(def_tasklist)
    #     return feature, tasklist

    # def load_user_data(self, user_id):
    #     user_path = None
    #     with open(user_path + 'feature.pkl', 'rb') as f:
    #         feature = joblib.load(f)
    #     tasklist = pd.read_csv(user_path + 'tasklist.csv')
    #     return feature, tasklist

    # def save(self, user_id):
    #     user_path = None
    #     feature = None
    #     tasklist = None

    #     with open(user_path + 'feature.pkl', 'wb') as f:
    #         joblib.dump(feature, f)
    #     tasklist.to_csv(user_path + 'tasklist.csv', index=False)

    def able_to_task(self, user_id):
        able = self.users_table.loc[user_id].max_count_of_task >= self.users_table.loc[user_id].number_of_tasks - 1
        return able

    def make_task(self, user_id, data):
        user_path = self.make_user_path(user_id)
        tasklist_path = user_path+'tasklist.csv'
        tasklist = self.get_tasklist(user_id)
        day_for = data['day_for']
        task_dead_line = time() + 60*60*24*day_for 
        
        new_task = def_tasklist.copy()
        new_task['name'] = data['name']
        new_task['day_for'] = day_for
        new_task['dead_line'] = task_dead_line
        new_task['status'] = 'play'
        tasklist = tasklist.append(new_task, ignore_index=True)
        tasklist.to_csv(tasklist_path, index=False)

        self.users_table.loc[user_id]['number_of_tasks'] += 1

    def save(self):
        self.users_table.to_csv(path_to_users)
        print('saved')

if __name__ == '__main__':
    A = Users()