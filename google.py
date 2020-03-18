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

MyBot = 'Mybot-9655a9770da5.json'
Credentials = ServiceAccountCredentials(MyBot, ['googleapis.com/auth/drive','googleapis.com/auth/spreadsheets']) #сформировали запрос
Authorize=Credentials.authorize(httplib2.Http()) # отсылаем запрос выше и авторизируемся
apib = apiclient.discovery.build('sheets', 'v4', http=Authorize)# обращаемся к конкретному апи и указываем его ваерсию, отсылаем токен авторизации
google_id='1YL1pTud53TsPTPbL81aSOJjNclyDq1n-xpDbyRcjMTI'



def Counter(apib,spredsheetid):
    apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid,body=
        {'valueInputOption':'User_Entered','data':[{'range': "'users'!J1", 'majorDimention':'ROUS','values':[['=COUNTA(A:A)']]}]}
                                        ).execute()
    strI=apib.spredsheets().values().get(spredsheetId=spredsheetid,majorDimention='ROUS', range="'users'!J1").execute()['values'][0][0] #кол во строк
    counter=dict()
    strI=apib.spredsheets().values().get(spredsheetId=spredsheetid,majorDimention='ROUS', range=f"'users'!A2-H{strI}").execute()['values']
    for j,i in enumerate(strI):
        if i[7] in counter:
            counter[i[7]][0] += float(i[6])
            counter[i[7]][1] += 1
        else: counter[i[7]] = [float(i[6]), 1]
        apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
        {'valueInputOption': 'User_Entered',
         'data': [{'range': f"'users'!G{j+1}", 'majorDimention': 'ROUS', 'values': [['0']]}]}
                                                ).execute()
    strI = apib.spredsheets().values().get(spredsheetId=spredsheetid, majorDimention='ROUS', range="'team'!J1").execute()['values'][0][0]
    strI = apib.spredsheets().values().get(spredsheetId=spredsheetid, majorDimention='ROUS', range=f"'team'!A2-C{strI}").execute()['values']
    for i,j in enumerate(strI):
        sum_balls=counter[j[0]][0]/2/counter[j[0]][1]*100
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
        apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid,body=
    {'valueInputOption':'User_Entered','data':[{'range': f"'users'!B{i}", 'majorDimention':'ROUS','values':[[f'{j[2]+team_ball}']]}]}
                                        ).execute()
        total = apib.spredsheets().values().get(spredsheetId=spredsheetid, majorDimention='ROUS', range=f"'team'!C{i}").execute()[
            'values'][0][0]
        apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
        {'valueInputOption': 'User_Entered',
         'data': [{'range': f"'users'!C{i}", 'majorDimention': 'ROUS', 'values': [[f'{j[2] + team_ball+total}']]}]}
                                                ).execute()



    def Counter_d():
        apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
        {'valueInputOption': 'User_Entered',
         'data': [{'range': "'users'!J1", 'majorDimention': 'ROUS', 'values': [['=COUNTA(A:A)']]}]}
                                                ).execute()
        strI = apib.spredsheets().values().get(spredsheetId=spredsheetid, majorDimention='ROUS', range="'users'!J1").execute()[
            'values'][0][0]  # кол во строк

        strI = apib.spredsheets().values().get(spredsheetId=spredsheetid, majorDimention='ROUS',
                                               range=f"'users'!A2-H{strI}").execute()['values']
        for j, i in enumerate(strI):
            if i[4] != day_t():
                apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
                {'valueInputOption': 'User_Entered',
                 'data': [{'range': f"'users'!D{j+1}", 'majorDimention': 'ROUS', 'values': [[f'{i[3] + 1}']]}]}
                                                        ).execute()

    def getpicture(user_id, ball, debt): # баллы ставятся каждому пользователю
        #users.loc[users['id'] == user_id, 'штраф'] += ball
        apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
        {'valueInputOption': 'User_Entered',
         'data': [{'range': "'users'!J1", 'majorDimention': 'ROUS', 'values': [['=COUNTA(A:A)']]}]}
                                                ).execute()
        strI = apib.spredsheets().values().get(spredsheetId=spredsheetid, majorDimention='ROUS', range="'users'!J1").execute()[
            'values'][0][0]

        strI = apib.spredsheets().values().get(spredsheetId=spredsheetid, majorDimention='ROUS',
                                               range=f"'users'!A2-H{strI}").execute()['values']
        for j,i in enumerate(strI):
            if i[1] == str(user_id):
                apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
                {'valueInputOption': 'User_Entered',
                 'data': [{'range': f"'users'!G{j+1}", 'majorDimention': 'ROUS', 'values': [[f'{i[6] + ball }']]}]}
                                                        ).execute()
                break
        #team.loc[team['команда'].values == users[users['id'] == user_id]['команда'].values, 'баллы за день'] += ball
        if debt == 0:
            #users.loc[users['id'] == user_id, 'дата'] = day_t()
            apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
            {'valueInputOption': 'User_Entered',
             'data': [{'range': f"'users'!E{j+1}", 'majorDimention': 'ROUS', 'values': [[f'{day_t()}']]}]}
                                                    ).execute()
        elif debt == 2:
            apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
            {'valueInputOption': 'User_Entered',
             'data': [{'range': f"'users'!F{j+1}", 'majorDimention': 'ROUS', 'values': [[f'{day_t()}']]}]}
                                                    ).execute()
        elif debt == 1:
            #users.loc[users['id'] == user_id, 'штраф'] -= 1
            apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
            {'valueInputOption': 'User_Entered',
             'data': [{'range': f"'users'!D{j+1}", 'majorDimention': 'ROUS', 'values': [[f'{int(i[3])-1}']]}]}
                                                    ).execute()
def Competition(apib,spredsheetid):
    apib.spredsheets().values().clear(spredsheetId=spredsheetid, range=f"'users'!F:F").execute()
    apib.spredsheets().values().batchUbdate(spredsheetId=spredsheetid, body=
            {'valueInputOption': 'User_Entered',
             'data': [{'range': f"'users'!F1", 'majorDimention': 'ROUS', 'values': ['конкурс']}]}
                                                    ).execute()