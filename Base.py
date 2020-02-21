import pandas as pd
from datetime import datetime

def day_t(): # передает актуальный день
    today = datetime.today()
    days=today.day
    #print (days)
    return days

def hour_t(): # передает актуальный день
    today = datetime.today()
    hour=today.hour*60+today.minute
    #print (days)
    return hour

def Data(id):
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    return users[users['id'] == id]['дата'].iloc[0]

def Debt(id):
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    return users[users['id'] == id]['долги'].iloc[0]



def Counter_d():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    users.loc[users['дата'] != day_t(), 'долги'] += 1
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.to_csv('users.csv', sep=';', encoding='windows-1251')


def getpicture(user_id,ball,debt):
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    #teams = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    print(users.head())
    users.loc[users['id'] == user_id, 'баллы'] += ball
    if debt==False:
        users.loc[users['id'] == user_id, 'долги'] = day_t()
    else:
        users.loc[users['id'] == user_id, 'долги'] -= 1
    print(users.head())
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.to_csv('users.csv', sep=';', encoding='windows-1251')





def Counter():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    teams = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    t=users.groupby(['команды']).agg({'баллы': 'sum', 'id': 'count'}).reset_index()
    for i in t['команды']:
        sum_balls = t[t['команды'] == i]['баллы']/2*day_t() / 2*t[t['команды'] == i]['id']
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

def Save(users, teams):
    users=pd.read_excel(users, encoding='windows-1251')
    teams = pd.read_excel(teams, encoding='windows-1251')
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.to_csv('users.csv', sep=';', encoding='windows-1251')
    teams = users.drop('Unnamed: 0', axis=1, errors='ignore')
    teams.to_csv('team.csv', sep=';', encoding='windows-1251')
