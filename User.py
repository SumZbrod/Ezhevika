from config import *
import joblib
import numpy as np
from datetime import datetime as dt 
import os

class Users:
    def __init__(self) -> None:
        self.users = pd.read_csv(path_to_users)
        self.users.set_index('user_id', inplace=True)

    def user_check(self, user_id, create=True):
        if user_id not in self.users.index:
            print('creatinf user')
            new_user = def_user.copy()
            new_user['user_id'] = user_id
            self.users = self.users.append(new_user, ignore_index=True)
            user_path = f'{path_to_data}{user_id}/'
            if not os.path.exists(user_path):
                os.makedirs(user_path)
            pd.DataFrame(def_tasklist).to_csv(f'{user_path}tasklist.csv', index=False)
            self.save()
        else:
            print('user exists')

    def default_data(self, ):
        feature = def_feature.copy()
        tasklist = pd.DataFrame(def_tasklist)
        return feature, tasklist

    def load_user_data(self, user_id):
        user_path = None
        with open(user_path + 'feature.pkl', 'rb') as f:
            feature = joblib.load(f)
        tasklist = pd.read_csv(user_path + 'tasklist.csv')
        return feature, tasklist

    def save(self, user_id):
        user_path = None
        feature = None
        tasklist = None

        with open(user_path + 'feature.pkl', 'wb') as f:
            joblib.dump(feature, f)
        tasklist.to_csv(user_path + 'tasklist.csv', index=False)

    def make_task(self, user_id):
        feature = None
        tasklist = None

        task_title = input('title: ')
        while True:
            task_day_for = input('day_for: ')
            if task_day_for.replace('.', '').isnumeric():
                task_day_for = float(task_day_for)
                if task_day_for > feature['skills']['max_days_for_task']:
                    print('to many days') 
                else:
                    break
            else:
                print(f'"{task_day_for}" is not a number')
        task_dead_line = None
        while True:
            task_status = input(f'status {statuses_for_task[:2]}: ')
            if task_status in statuses_for_task[:2]:
                break
            else:
                print(f'status can be only like: {statuses_for_task[:2]}')
        
        new_task = def_tasklist.copy()
        new_task['title'] = task_title
        new_task['day_for'] = task_day_for
        new_task['dead_line'] = task_dead_line
        new_task['status'] = task_status
        tasklist = tasklist.append(new_task, ignore_index=True)
    
    def save(self):
        self.users.to_csv(path_to_users)
        print('saved')
if __name__ == '__main__':
    A = Users()