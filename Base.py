import pandas as pd
from datetime import datetime
import os
def getpicture(user_id,ball):
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    #teams = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    print(users.head())
    users.loc[users['id']==user_id, 'баллы']+=ball
    print(users.head())
    users.to_csv('users.csv', sep=';', encoding='windows-1251')



def day_t(): # передает актуальный день
    today = datetime.today()
    days=today.day
    #print (days)
    return days



def Counter():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    teams = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    t=users.groupby(['команды']).agg({'баллы': 'sum', 'id': 'count' }).reset_index()
    for i in t['команды']:
        sum_balls = t[t['команды'] == i]['баллы']/day_t() / t[t['команды'] == i]['id']
        sum_balls = sum_balls.iloc[0]*100
        if sum_balls == 100:  # над отестить оптимальное количество баллов
            team_ball = 12
        elif sum_balls >= 90:
            team_ball = 9
        elif sum_balls > 80:
            team_ball = 8
        elif sum_balls > 70:
            team_ball = 7
        elif sum_balls > 60:
            team_ball = 6
        elif  sum_balls > 50:
            team_ball = 5
        else:
            team_ball = 0
        teams.loc[teams['им команды'] == i, 'баллы общие'] += team_ball

    print(teams.head())
