from config import *
import joblib
import numpy as np
from datetime import datetime as dt 

class Users:
    def __init__(self, user_id) -> None:
        if self.user_exist():
            self.make_new_user()

        feature, tasklist = self.load_user_data()
            
        self.user_path = path_to_data + str(user_id) + '/'
        self.feature = feature
        self.tasklist = tasklist

    def create_user(self):
        users_df = pd.read_csv(path_to_users, )
        while True:
            user_id = np.random.randint(*random_id)
            if user_id not in users_df.index:
                break
        return user_id

    def default_data(self):
        feature = def_feature.copy()
        tasklist = pd.DataFrame(def_tasklist)
        return feature, tasklist

    def load_user_data(self, user_id):
        with open(self.user_path + 'feature.pkl', 'rb') as f:
            feature = joblib.load(f)
        tasklist = pd.read_csv(self.user_path + 'tasklist.csv')
        return feature, tasklist

    def save(self):
        with open(self.user_path + 'feature.pkl', 'wb') as f:
            joblib.dump(self.feature, f)
        self.tasklist.to_csv(self.user_path + 'tasklist.csv', index=False)

    def make_task(self):
        task_title = input('title: ')
        while True:
            task_day_for = input('day_for: ')
            if task_day_for.replace('.', '').isnumeric():
                task_day_for = float(task_day_for)
                if task_day_for > self.feature['skills']['max_days_for_task']:
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
        self.tasklist = self.tasklist.append(new_task, ignore_index=True)
        self.save()

if __name__ == '__main__':
    A = User()
    print(A.user_id)
    A.make_task()
    print(A.tasklist)