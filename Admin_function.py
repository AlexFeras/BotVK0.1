import pandas as pd

def get_Admin_statistic():
    team = pd.read_csv('team.csv', sep=';', encoding='windows-1251', engine='python')
    for index,row in team.sort_values('баллы общие',ascending=False).reset_index(drop=True).iterrows():
        yield row['им команды'],row["баллы за день"],row['баллы общие']