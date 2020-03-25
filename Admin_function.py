import pandas as pd
from Base import getpicture, Counter, day_t, hour_t,Counter_d,Data,Debt,Save

def get_Admin_statistic(t=None):
    team = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    if t != None:
        t=list(users.loc[users['id']==t, 'команда'])[0]
        team=team[team["команда"]==t]
    for index,row in team.sort_values('баллы общие',ascending=False).reset_index(drop=True).iterrows():
        yield f' Команда {row["команда"]} \n Баллы за день {row["баллы за день"]} \n Общие баллы {row["баллы общие"]}'


def Get_stat(t=None): # для админа ничего не передавать в параметр, для старосты команду
    team = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    if t != None:
        users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
        t = list(users.loc[users['id'] == t, 'команда'])[0]
        team=team[team['команда'] == t]
    return ' '.join(map(lambda x: '@id'+str(x),list(team[team['дата']!=day_t()]['id'])))

def Info_debt(t=None):
    team = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    if t != None:
        users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
        t = list(users.loc[users['id'] == t, 'команда'])[0]
        team = team[team['команда'] == t]
    for i in  list(team['команда']):
        t1=team[[team["команда"]==i] and team["дата"]==day_t()].shape[0]
        t2=team[[team["команда"]==i] and team["дата"]!=day_t()].shape[0]
        yield f'Команда {i} \n Сдали {t1 if t1 else 0} \n Не сдали{t2 if t2 else 0}'

def clean_challenge():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    users.loc[:,'На конкурс']=0
    users = users.drop('Unnamed: 0', axis=1, errors='ignore')
    users.to_csv('users.csv', sep=';', encoding='windows-1251')

def chellenge():
    users = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    users=users[users['На конкурс']!=0]
    for index, row in users.sort_values('На конкурс', ascending=False).reset_index(drop=True).iterrows():
        yield f' Команда {row["команда"]} \n Баллы на конкурс {row["На конкурс"]} \n @id{row["id"]}'





