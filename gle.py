from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import apiclient
from datetime import datetime
from collections import defaultdict

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

def Counter(apib,spreadsheetid):
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid,body=
        {'valueInputOption':'User_Entered','data':[{'range': "'users'!J1", 'majorDimension':'ROWS','values':[['=COUNTA(A:A)']]}]}
                                        ).execute()
    strI=apib.spreadsheets().values().get(spreadsheetId=spreadsheetid,majorDimension='ROWS', range="'users'!J1").execute()['values'][0][0] #кол во строк
    counter=dict()
    strI=apib.spreadsheets().values().get(spreadsheetId=spreadsheetid,majorDimension='ROWS', range=f"'users'!A2:H{strI}").execute()['values']
    for j,i in enumerate(strI):
        if i[7] in counter:
            counter[i[7]][0] += float(i[6])
            counter[i[7]][1] += 1
        else: counter[i[7]] = [float(i[6]), 1]
        apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
        {'valueInputOption': 'User_Entered',
         'data': [{'range': f"'users'!G{j+2}", 'majorDimension': 'ROWS', 'values': [['0']]}]}
                                                ).execute()
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'team'!J1").execute()['values'][0][0]
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range=f"'team'!A2:C{strI}").execute()['values']
    for i,j in enumerate(strI):
        sum_balls=counter[j[0]][0]/2/counter[j[0]][1]*10 # формула подсчёта
        apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid,body=
    {'valueInputOption':'User_Entered','data':[{'range': f"'users'!B{i+2}", 'majorDimension':'ROWS','values':[[f'{float(j[2])+sum_balls}']]}]}
                                        ).execute()
        total = apib.spredsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range=f"'team'!C{i+2}").execute()[
            'values'][0][0]
        apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
        {'valueInputOption': 'User_Entered',
         'data': [{'range': f"'users'!C{i+2}", 'majorDimension': 'ROWS', 'values': [[f'{float(j[2]) + sum_balls+total}']]}]}
                                                ).execute()



def Counter_d(apib,spreadsheetid):
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
    {'valueInputOption': 'User_Entered',
     'data': [{'range': "'users'!J1", 'majorDimension': 'ROWS', 'values': [['=COUNTA(A:A)']]}]}
                                            ).execute()
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'users'!J1").execute()[
        'values'][0][0]  # кол во строк

    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS',
                                           range=f"'users'!A2:H{strI}").execute()['values']
    for j, i in enumerate(strI):
        if i[4] != day_t():
            apib.spreadsheets().values().batchUbdate(spredsheetId=spreadsheetid, body=
            {'valueInputOption': 'User_Entered',
             'data': [{'range': f"'users'!D{j+1}", 'majorDimension': 'ROWS', 'values': [[f'{float(i[3]) + 1}']]}]}
                                                    ).execute()

def getpicture(user_id, ball, debt,apib,spreadsheetid): # баллы ставятся каждому пользователю
    #users.loc[users['id'] == user_id, 'штраф'] += ball
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
    {'valueInputOption': 'User_Entered',
     'data': [{'range': "'users'!J1", 'majorDimension': 'ROWS', 'values': [['=COUNTA(A:A)']]}]}
                                            ).execute()
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'users'!J1").execute()[
        'values'][0][0]

    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS',
                                           range=f"'users'!A2:H{strI}").execute()['values']
    for j,i in enumerate(strI):
        if i[1] == str(user_id):#batchUpdate записать get получить данные
            apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body={'valueInputOption': 'User_Entered',
             'data': [{'range': f"'users'!G{j+2}", 'majorDimension': 'ROWS', 'values': [[f'{float(i[6]) + ball }']]}]}
                                                    ).execute()
            break
    #team.loc[team['команда'].values == users[users['id'] == user_id]['команда'].values, 'баллы за день'] += ball
    if debt == 0:
        #users.loc[users['id'] == user_id, 'дата'] = day_t()
        apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
        {'valueInputOption': 'User_Entered',
         'data': [{'range': f"'users'!E{j+2}", 'majorDimension': 'ROWS', 'values': [[f'{day_t()}']]}]}
                                                ).execute()
    elif debt == 2:
        apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
        {'valueInputOption': 'User_Entered',
         'data': [{'range': f"'users'!F{j+2}", 'majorDimension': 'ROWS', 'values': [[f'{day_t()}']]}]}
                                                ).execute()
    elif debt == 1:
        #users.loc[users['id'] == user_id, 'штраф'] -= 1
        apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
        {'valueInputOption': 'User_Entered',
         'data': [{'range': f"'users'!D{j+2}", 'majorDimension': 'ROWS', 'values': [[f'{int(i[3])-1}']]}]}
                                                ).execute()
def Competition(apib,spreadsheetid):
    apib.spreadsheets().values().clear(spreadsheetId=spreadsheetid, range=f"'users'!F:F").execute()
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body={'valueInputOption': 'User_Entered','data': [{'range': f"'users'!F1", 'majorDimension': 'ROWS', 'values': [['конкурс']]}]}).execute()

def user_in_base(user_id,apib,spreadsheetid): #исключение
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
    {'valueInputOption': 'User_Entered','data': [{'range': f"'users'!J1", 'majorDimension': 'ROWS','values': [[f'=IF(ISERROR(MATCH({user_id};B:B;0));0;MATCH({user_id};B:B;0))']]}]}
                                             ).execute()
    strB = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'users'!J1").execute()['values'][0][0]
    return bool(int(strB))#заполнена ячейка или нет

def Data(user_id,apib,spreadsheetid):
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
    {'valueInputOption': 'User_Entered',
     'data': [{'range': f"'users'!J1", 'majorDimension': 'ROWS', 'values': [[f'=IF(ISERROR(MATCH({user_id};B:B;0));0;MATCH({user_id};B:B;0))']]}]}
                                             ).execute()
    strB=apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'users'!J1").execute()['values'][0][0]
    return int(apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range=f"'users'!E{int(strB)}").execute()['values'][0][0])

def Debt(user_id,apib,spreadsheetid):
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body={'valueInputOption': 'User_Entered',
     'data': [{'range': f"'users'!J1", 'majorDimension': 'ROWS',
               'values': [[f'=IF(ISERROR(MATCH({user_id};B:B;0));0;MATCH({user_id};B:B;0))']]}]} ).execute()
    strB = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'users'!J1").execute()['values'][0][0]
    return int(apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range=f"'users'!D{int(strB)}").execute()['values'][0][0])

def get_Admin_statistic(axess,apib,spreadsheetid):
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
    {'valueInputOption': 'User_Entered',
     'data': [{'range': "'team'!J1", 'majorDimension': 'ROWS', 'values': [['=COUNTA(A:A)']]}]}
                                             ).execute()
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'team'!J1").execute()['values'][0][0]
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range=f"'team'!A2:C{strI}").execute()['values']
    for i in strI:
        yield f' Команда {i[0]} \n Баллы за день {i[1]} \n Баллы общие{i[2]}'


    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
    {'valueInputOption': 'User_Entered',
     'data': [{'range': "'users'!J1", 'majorDimension': 'ROWS', 'values': [['=COUNTA(A:A)']]}]}
                                             ).execute()
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'users'!J1").execute()['values'][0][0]
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS',range=f"'users'!A2:H{strI}").execute()['values']
    yield f' Не сдали \n'
    some=0
    name=''
    strI.sort(key=lambda x: x[7])
    for i in strI:
        if name!=i[7]:
            name=i[7]
            yield f'Должников у команды {name}'
            some=0
        else:
            some+=0 if int(i[3])==0 else 1
        if int(i[3])!=0:
            yield f'@id{i[1]} Количество долгов {i[3]}'


def chellenge(axess,apib,spreadsheetid):
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
    {'valueInputOption': 'User_Entered',
     'data': [{'range': "'users'!J1", 'majorDimension': 'ROWS', 'values': [['=COUNTA(A:A)']]}]}
                                             ).execute()
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'users'!J1").execute()[
        'values'][0][0]
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS',
                                            range=f"'users'!A2:H{strI}").execute()['values']
    some = 0
    name = ''
    strI.sort(key=lambda x: x[7])
    for i in strI:
        if name != i[7]:
            name = i[7]
            yield f' Команда {name}-Сдали на конкурс '
            some = 0
        else:
            some += 0 if i[5] else 1
        if i[5]:
            yield f'@id{i[1]} '
            # yield f'@id{i[1]} Количество долгов {i[3]}'


def get_day_statistic(axess,apib,spreadsheetid):
    apib.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=
    {'valueInputOption': 'User_Entered',
     'data': [{'range': "'users'!J1", 'majorDimension': 'ROWS', 'values': [['=COUNTA(A:A)']]}]}
                                             ).execute()
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS', range="'users'!J1").execute()[
        'values'][0][0]
    strI = apib.spreadsheets().values().get(spreadsheetId=spreadsheetid, majorDimension='ROWS',
                                            range=f"'users'!A2:H{strI}").execute()['values']
    some = 0
    name = ''
    team=''
    strI.sort(key=lambda x: x[7])
    for i in strI:
        if name != i[7]:
            name = i[7]
            yield f' Команда {name} Не сдали'
            some = 0
        else:
            some += 0 if i[4] else 1
        for i[1] in i[7]:
            if int(i[4])!=day_t():
                yield f'@id{i[1]} '
            #yield f'@id{i[1]} Количество долгов {i[3]}'




