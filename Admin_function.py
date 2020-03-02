import pandas as pd
from Base import getpicture, Counter, day_t, hour_t,Counter_d,Data,Debt,Save
def get_Admin_statistic():
    team = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    for index,row in team.sort_values('баллы общие',ascending=False).reset_index(drop=True).iterrows():
        yield f' Команда {row["команда"]} \n Баллы за день {row["баллы за день"]} \n Общие баллы {row["баллы общие"]}'


def Get_stat(t=None): # для админа ничего не передавать в параметр, для старосты команду
    team = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    if t != None:
        team=team[team['команда'] == t]
    return ' '.join(map(str,list(team[team['дата']!=day_t()]['id'])))

def Info_debt(t=None):
    team = pd.read_csv('users.csv', sep=';', encoding='windows-1251', engine='python')
    if t != None:
        team = team[team['команда'] == t]
    for i in  list(team['команда']):
        t1=team[[team["команда"]==i] and team["дата"]==day_t()].shape[0]
        t2=team[[team["команда"]==i] and team["дата"]!=day_t()].shape[0]
        yield f'Команда {i} \n Сдали {t1 if t1 else 0} \n Не сдали{t2 if t2 else 0}'




