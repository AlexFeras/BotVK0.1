import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json
import requests
import wget
from gle import *
import os
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import googleapiclient.discovery
from random import choice,sample

if __name__ == "__main__": # будет 2 группы или передавать токен через ексель или как то иначе!!!!

    group_id = 191601892
    album_id = 270167491
    album_challenge_id=271211305
    vk_message = vk_api.VkApi(token=token)
    vk_photo = vk_api.VkApi(token=acess_token)
    v = '5.103'#версия приложения
    vk_message._auth_token()
    vk_message.get_api()
    vk_photo._auth_token()
    vk_photo.get_api()


    def get_button(label='but', color='red', payload=''):
        return {
            "action": {
                "type": 'text',
                'payload': payload,  # идентификатор кнопки
                'label': label
            },
            "color": color
        }

    keyboard = { #создаем клавиатуру
        "one_time": False,
        "buttons": [
            [get_button(label="Загрузить работу", color='secondary')],
            [get_button(label="Загрузить долг!", color='secondary'), get_button(label="Загрузить на батл", color='secondary')],[get_button(label="Правила", color='secondary')]
                    ]
    }
    keyboard_Leader = {
        "one_time": False,
        "buttons": [
            [get_button(label="Загрузить работу", color='secondary')],
            [get_button(label="Загрузить долг!", color='secondary'),
             get_button(label="Загрузить на батл", color='secondary')],
            [get_button(label="Правила", color='secondary')],
            [get_button(label="Статистика общая", color='secondary'),get_button(label="Статистика дня", color='secondary')]
        ]
    }
    keyboard_Admin = {
        "one_time": False,
        "buttons": [
            [get_button(label="Статистика общая", color='secondary'), get_button(label="Статистика дня", color='secondary')],
            [get_button(label="Начать челлендж", color='secondary')],[get_button(label="Получить результаты челленджа", color='secondary')]
        ]
    }
    keyboard = str(json.dumps(keyboard, ensure_ascii=False))
    keyboard_Leader = str(json.dumps(keyboard_Leader, ensure_ascii=False))
    keyboard_Admin = str(json.dumps(keyboard_Admin, ensure_ascii=False))


    def Leader(vk,keyboard_Leader):
        longpoll = VkBotLongPoll(vk, group_id)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if 'Статистика общая' in event.object.message['text']:
                    for i in get_Admin_statistic(0, apib, spreadsheetid):
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': i,
                                                            'random_id': 0})
                elif 'Статистика дня' in event.object.message['text']:
                    for i in get_day_statistic(0, apib, spreadsheetid):
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': i,
                                                            'random_id': 0})
                elif ("Загрузить работу" in event.object.message['text']) or ("1" in event.object.message[
                    'text']):  ## Как сделать так,чтобы бот передавал комментарий к рисунку вместе с рисуноком
                    if Data(event.object.message['peer_id'], apib, spreadsheetid) == day_t():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Вы уже сдавали работу! Ждём вас завтра!",
                                                            'random_id': 0})
                    else:

                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Загружай!",
                                                            'random_id': 0})

                        tmp = daylik(vk_message, keyboard, album_id)
                elif ("Загрузить долг!" in event.object.message['text']) or (
                        "2" in event.object.message['text']):  # если нажать на кнопку, то проиходйет это
                    if Debt(event.object.message['peer_id'], apib, spreadsheetid) <= 0:
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Вы сдали все долги!",
                                                            'random_id': 0})

                    else:
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Загружайте долг",
                                                            'random_id': 0})
                        tmp = debt_daylik(vk_message, keyboard)
                elif ("Загрузить на батл" in event.object.message['text']) or ("3" in event.object.message['text']):

                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': "Загружай на батл",
                                                        'random_id': 0})
                    tmp = daylik_competition(vk_message, keyboard)
                elif ("Правила" in event.object.message['text']) or ("0" in event.object.message['text']):  # НЕ ГОТОВО
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': "https://vk.com/public191601892?w=wall-191601892_2",
                                                        # тут правила
                                                        'random_id': 0})
                elif 'Назад' in event.object.message['text']:
                    break


    def Admin_app_team(vk,name,both):
        longpoll = VkBotLongPoll(vk, group_id)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message['attachments'] and both == True:
                    if event.object.message['attachments'][0]['type'] == 'doc':  # новая база
                        url_team = event.object.message['attachments'][0]['doc']['url']
                        file_team = wget.download(url_team)
                        #Save(file_team,name)
                        os.remove(file_team)
                        break
                elif len(event.object.message['attachments']) and both == False:
                    if event.object.message['attachments'][0]['type'] == 'doc':  # новая база
                        url_team = event.object.message['attachments'][0]['doc']['url']
                        file_team = wget.download(url_team)
                        #Save(file_team, 'user.csv')
                        os.remove(file_team)
                    if event.object.message['attachments'][1]['type'] == 'doc':  # новая база
                        url_team = event.object.message['attachments'][1]['doc']['url']
                        file_team = wget.download(url_team)
                        #Save(file_team, 'team.scv')
                        os.remove(file_team)
                else: break
    def Admin(vk,keyboard_Admin):
        global album_challenge_id
        longpoll = VkBotLongPoll(vk, group_id)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message['text'].lower() == 'Админ_начать':  # обратились к сообщению, образаемся к "тексту"
                    vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                                        'message': 'ok',
                                                        'random_id': 0, 'keyboard': keyboard_Admin})
                elif 'Статистика общая' in event.object.message['text']: # НЕОБХОДИМО ПОЛУЧИТЬ КАКИЕ УЧАСТНИКИ И ИЗ КАКОЙ КОМАНДЫ. ИМЯ И ID  ID в формате "id@1233255"
                    for i in get_Admin_statistic(0,apib,spreadsheetid):
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': i,
                                                            'random_id': 0})
                elif 'Статистика дня' in event.object.message['text']:
                    for i in get_day_statistic(0, apib, spreadsheetid):
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': i,
                                                            'random_id': 0})
                elif 'Начать челлендж' in event.object.message['text']:# ГОТОВО
                    Competition(apib,spreadsheetid)
                    album_challenge_id = vk_photo.method('photos.createAlbum',{'title': str(day_t()) + " День. Челлендж", 'group_id': group_id})['id']# создает альбом для конкурсов
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': "Альбом для конкурса создан",
                                                        'random_id': 0})
                elif 'Получить результаты челленджа' in event.object.message['text']: #нету
                    for i in chellenge(0,apib,spreadsheetid):
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': f'{i}',
                                                            'random_id': 0})

                elif 'Назад' in event.object.message['text']:
                    break
    def photo(body,user_id, url, group_id, album_id):
        file = wget.download(url)
        upload_url = vk_photo.method('photos.getUploadServer', {'group_id': group_id, 'album_id':

            album_id})['upload_url']
        info = requests.post(upload_url, files={'photo': open(file, 'rb')}).json()
        t=vk_photo.method('photos.save',
                        {'server': info['server'], 'photos_list': info['photos_list'], 'aid': info['aid'],
                         'hash': info['hash'], 'group_id': group_id, 'album_id': album_id, 'caption': body})
        os.remove(file)
        return t
    def daylik(vk,keyboard,album_id):
        longpoll = VkBotLongPoll(vk, group_id)
        flag2 = 0
        for event in longpoll.listen():
            if (hour_t() >= 1320) and (hour_t() < 1380):
                flag2 = 1
            elif hour_t() >= 1385:
                if flag2 != 0:
                    Counter() # считает раз в день
                    flag2 = 0
                    album_id = vk_photo.method('photos.createAlbum',
                                               {'title': str(day_t() + 1) + " День", 'group_id': group_id})['id']
            else:
                if flag2 != 0:
                    Counter_d()
                    #Delete_us()
                    flag2 = 0
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message['attachments']:
                    if event.object.message['attachments'][0]['type'] == 'photo':  # photo
                        url = event.object.message['attachments'][0]['photo']['sizes'][6]['url']
                        messages = vk_message.method("messages.getConversations",
                                                     {'offset': 0, 'count': 20, 'filter': 'unread'})
                        file = wget.download(url)
                        id = event.object.message['peer_id']
                        body = event.object.message['text']
                        k=photo(body,id, url, group_id, album_id)
                        if flag2 == 0:
                            getpicture(event.object.message['peer_id'], 2, False,apib,spreadsheetid)
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Отлично, работа принята!",
                                                                'random_id': 0})
                        if flag2 == 1:
                            getpicture(event.object.message['peer_id'], 1, False,apib,spreadsheetid)
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Отлично, работа принята! Не опаздывай больше)",
                                                                'random_id': 0})
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': f"https://vk.com/album-{group_id}_{album_id}" ,
                                                                'random_id': 0})
                        if flag2 == 2:
                            getpicture(event.object.message['peer_id'], 0, False,apib,spreadsheetid)
                        os.remove(file)
                        for i in range(1,len(event.object.message['attachments'])):
                            url = event.object.message['attachments'][i]['photo']['sizes'][6]['url']
                            file = wget.download(url)
                            upload_url = vk_photo.method('photos.getUploadServer', {'group_id': group_id, 'album_id': album_id})['upload_url']
                            info = requests.post(upload_url, files={'photo': open(file, 'rb')}).json()
                            vk_photo.method('photos.createComment',
                                            {'owner_id':-group_id,'photo_id':k[0]['id'], "attachments": f'photo{-group_id}_{event.object.message["attachments"][i]["photo"]["id"]}'})
                            # vk_photo.method('photos.createComment',
                            #                                  {'owner_id':-group_id,'photo_id':k[0]['id'], "message": "Это кот " }) # комментарии
                            os.remove(file)


                        return event
                    if "Назад" in event.object.message['text']:
                        break
    def debt_daylik(vk,keyboard):
        longpoll = VkBotLongPoll(vk, group_id)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                   if event.object.message['attachments']:
                        if event.object.message['attachments'][0]['type'] == 'photo':  # photo
                            vk_message.method('messages.getConversations',
                                              {"peer_id": event.object.message['peer_id'],
                                               'message': "",
                                               'attachment': 'photo-191561475_457239022',
                                               'random_id': 0})
                            url = event.object.message['attachments'][0]['photo']['sizes'][6]['url']
                            messages = vk_message.method("messages.getConversations",
                                                         {'offset': 0, 'count': 20, 'filter': 'unread'})
                            id = event.object.message['peer_id']  # id отправителя
                            body = event.object.message['text']  # сам текст
                            photo(body,id, url, group_id, album_id)
                            getpicture(event.object.message['peer_id'], 0.5, True,apib,spreadsheetid)
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Отлично, долг принят!",
                                                                'random_id': 0})
                        return event
                   if "Назад" in event.object.message['text']:
                        break
    def daylik_competition(vk,keyboard):
            longpoll = VkBotLongPoll(vk, group_id)
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.object.message['attachments']:
                        if event.object.message['attachments'][0]['type'] == 'photo':  # photo
                            vk_message.method('messages.getConversations',
                                        {"peer_id": event.object.message['peer_id'],  # выведет ок если пришло фото
                                            'message': "",

                                            'random_id': 0})
                            url = event.object.message['attachments'][0]['photo']['sizes'][6]['url']
                            messages = vk_message.method("messages.getConversations",
                                                    {'offset': 0, 'count': 20, 'filter': 'unread'})
                            id = event.object.message['peer_id']  # id отправителя
                            body = event.object.message['text']  # сам текст
                            #album_Com_id = vk_photo.method('photos.createAlbum',# создает альбом для конкурсов
                            #                           {'title': str(day_t() + 1) + " День. Конкурсы, ", 'group_id': group_id})['id']
                            photo(body,id, url, group_id, album_challenge_id)
                            getpicture(event.object.message['peer_id'], 0, 2,apib,spreadsheetid)
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Отлично, работа принята!",
                                                                'random_id': 0})
                        return event
                    if "Назад" in event.object.message['text']:
                        break


    longpoll = VkBotLongPoll(vk_message, group_id) #событие, наблюдаем за некоторой событийной модель
    tmp = type('vk', (), {'object': type('mes', (), {'message': {'peer_id': 0, 'id': 0}})})
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if user_in_base(event.object.message['peer_id'],apib,spreadsheetid):
                if event.object.message['text'].lower() == 'начать':# обратились к сообщению, образаемся к "тексту"
                    a = vk_message.method('users.get', {'user_ids': event.object.message['peer_id']})
                    a = a[0]['first_name']
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': 'Привет, друг ' + str(a),
                                                        'random_id': 0})
                    vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                                'message': ' Нажми на кнопку или напиши необходимую команду,если кнопки не работают \n 0.Правила. \n 1. Загрузить работу.\n 2.Загрузить долг!.\n 3. Загрузить на батл',
                                                'random_id': 0, 'keyboard': keyboard})
                elif ("Загрузить работу" in event.object.message['text']) or ("1" in event.object.message['text']):## Как сделать так,чтобы бот передавал комментарий к рисунку вместе с рисуноком
                     if Data(event.object.message['peer_id'],apib,spreadsheetid)==day_t():
                         vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                             'message': "Вы уже сдавали работу! Ждём вас завтра!",
                                                             'random_id': 0})
                     else:

                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                 'message': "Загружай!",
                                                 'random_id': 0})

                        tmp = daylik(vk_message, keyboard, album_id)
                elif ("Загрузить долг!" in event.object.message['text']) or ("2" in event.object.message['text']):  # если нажать на кнопку, то проиходйет это
                    if Debt(event.object.message['peer_id'],apib,spreadsheetid) <=0:
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Вы сдали все долги!",
                                                            'random_id': 0})

                    else:
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Загружайте долг",
                                                            'random_id': 0})
                        tmp = debt_daylik(vk_message,keyboard)
                elif ("Загрузить на батл" in event.object.message['text']) or ("3" in event.object.message['text']):

                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                 'message': "Загружай на батл",
                                                 'random_id': 0})
                    tmp=daylik_competition(vk_message,keyboard)
                elif ("Правила" in event.object.message['text']) or ("0" in event.object.message['text']):  # НЕ ГОТОВО
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "https://vk.com/public191601892?w=wall-191601892_2", # тут правила
                                                            'random_id': 0})
                elif event.object.message['text'].lower() == 'начать_староста': #староста БУДЕТ ЛИ ОН ПРИНИМАТЬ УЧАСТИЕ В ДЕЙЛИКАХ? НАДО ЛИ ДОБАВИТЬ СЮДА ФУНКЦЙИИ ИЛИ ВСЁ И ТАК БУДЕТ РАБОТАТЬ?
                    a = vk_message.method('users.get', {'user_ids': event.object.message['peer_id']})
                    a = a[0]['first_name']
                    vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                                        'message': 'Привет, староста  '+str(a),
                                                        'random_id': 0, 'keyboard': keyboard_Leader})
                    Leader(vk_message,keyboard_Leader)
                elif event.object.message['text'].lower() == 'начать_админ':
                    a = vk_message.method('users.get', {'user_ids': event.object.message['peer_id']})
                    a = a[0]['first_name']
                    vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                                        'message': 'Привет, администратор  '+str(a),
                                                        'random_id': 0, 'keyboard': keyboard_Admin})
                    Admin(vk_message,keyboard_Admin)
                else:
                    if not ((tmp.object.message['peer_id'] == event.object.message['peer_id']) and (tmp.object.message['id'] == event.object.message['id'])):
                        if event.object.message['attachments']:
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': ' Нажми на кнопку или напиши необходимую команду,если кнопки не работают \n 0.Правила. \n 1. Загрузить работу.\n 2.Загрузить долг!.\n 3. Загрузить на батл',
                                                                'random_id': 0})
                        else:
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Напечатай слово <начать>,чтобы приступить к работе",
                                                                'random_id': 0})
            else:
                vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                    'message': "Вы  были исключены из дейликов",
                                                    'random_id': 0})



