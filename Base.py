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
    return users[users['id'] == id]['Штрафные баллы'].iloc[0]



def Counter_d():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    users.loc[users['дата'] != day_t(), 'долги'] += 1
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.to_csv('users.csv', sep=';', encoding='windows-1251')


def getpicture(user_id,ball,debt):
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    team = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    print(users.head())
    users.loc[users['id'] == user_id, 'баллы'] += ball
    team.loc[team[team['команды']==users[users['id'] == user_id]['команды']].loc[0], 'баллы за день'] += ball
    if debt==0:
        users.loc[users['id'] == user_id, 'дата'] = day_t()
    elif debt==1:
        users.loc[users['id'] == user_id, 'долги'] -= 1
    print(users.head())
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.to_csv('users.csv', sep=';', encoding='windows-1251')
    team.to_csv('team.csv', sep=';', encoding='windows-1251')


def Counter():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    teams = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    t=users.groupby(['команды']).agg({'баллы': 'sum', 'id': 'count'}).reset_index()
    for i in t['команды']:
        sum_balls = t[t['команды'] == i]['баллы']/2*day_t() / t[t['команды'] == i]['id']
        sum_balls = sum_balls.iloc[0]*100
        if sum_balls == users[users['команды']==i].shape[0]:  # над отестить оптимальное количество баллов
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
        teams.loc[teams['Имя команды'] == i, 'баллы общие'] += team_ball

    print(teams.head())

def Save(teams,name):
    teams = pd.read_excel(teams,sep=';',encoding='windows-1251')
    teams = teams.drop('Unnamed: 0', axis=1, errors='ignore')
    teams.to_csv(name, sep=';', encoding='windows-1251')

def Delete_us():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.drop(users[users['баллы']<=day_t()*2*0.7].index,inplace=True)#если ниже 70 процентов от макс балла, то кик
    users.to_csv('users.csv', sep=';', encoding='windows-1251')
