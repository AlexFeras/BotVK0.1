import pandas as pd
from datetime import datetime

def day_t(): # передает актуальный день
    today = datetime.today()
    days=today.day
    #print (days)
    return days

def hour_t(): # передает актуальный час(внутри перевод в минуты)
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
    users.loc[users['дата'] != day_t(), 'Штрафные баллы'] += 1
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.to_csv('users.csv', sep=';', encoding='windows-1251')


def getpicture(user_id, ball, debt):
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    team = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    print(users.head())
    users.loc[users['id'] == user_id, 'Штрафные баллы'] += ball
    team.loc[team['команда'].values == users[users['id'] == user_id]['команда'].values, 'баллы за день']+= ball
    if debt==0:
        users.loc[users['id'] == user_id, 'дата'] = day_t()
    elif debt==2:
        users.loc[users['id'] == user_id, 'На конкурс'] = day_t()
    elif debt==1:
        users.loc[users['id'] == user_id, 'Штрафные баллы'] -= 1
    print(users.head())
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    team=team.drop('Unnamed: 0', axis=1, errors='ignore')
    users.to_csv('users.csv', sep=';', encoding='windows-1251')
    team.to_csv('team.csv', sep=';', encoding='windows-1251')


def Counter():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    teams = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    t=users.groupby(['команда']).agg({'баллы': 'sum', 'id': 'count'}).reset_index()
    for i in t['команда']:
        sum_balls = t[t['команда'] == i]['баллы']/ 2*t[t['команда'] == i]['id'] # как сделать так,чтобы в 23-00 он очищал столбик и по новой заполнял в след день.
        sum_balls = sum_balls.iloc[0]*100
        if sum_balls == 100:
            team_ball = 10
        elif sum_balls >= 98:
            team_ball = 9
        elif sum_balls > 96:
            team_ball = 8
        elif sum_balls > 94:
            team_ball = 7
        elif sum_balls > 92:
            team_ball = 6
        elif  sum_balls > 90:
            team_ball = 5
        elif  sum_balls > 88:
            team_ball = 4
        elif  sum_balls > 86:
            team_ball = 3
        elif  sum_balls > 84:
            team_ball = 2
        elif  sum_balls > 82:
            team_ball = 1
        else:
            team_ball = 0
        teams.loc[teams['команда'] == i, 'баллы общие'] += team_ball

    print(teams.head())

def Save(teams,name):
    teams = pd.read_excel(teams,sep=';',encoding='windows-1251')
    teams = teams.drop('Unnamed: 0', axis=1, errors='ignore')
    teams.to_csv(name, sep=';', encoding='windows-1251')

def Delete_us():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.drop(users[day_t()*2-users['баллы']>=6].index,inplace=True)#СДЕЛАТЬ 3 ПРОПУСКА ИЛИ 6 ОПОЗДАНИЙ И КИК
    users.to_csv('users.csv', sep=';', encoding='windows-1251')

def Cleaner_tab():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.loc[:, 'баллы за день'] = 0
    users.to_csv('users.csv', sep=';', encoding='windows-1251')
def maximus():
    day_t()*2
    return
def user_in_base(peer_id): #исключение
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    return any(users['id'] == peer_id)
