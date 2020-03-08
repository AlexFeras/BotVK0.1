import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json
import requests
import wget
from Base1 import getpicture, Counter, day_t, hour_t,Counter_d,Data,Debt,Save,user_in_base,Delete_us
from Admin_function import get_Admin_statistic,Get_stat,Info_debt,chellenge
import os
from random import choice,sample


if __name__ == "__main__":# будет 2 группы или передавать токен через ексель или как то иначе!!!!

    group_id = 191601892
    album_id = 270167491
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
            [get_button(label="Правила", color='secondary')], [get_button(label="Загрузить работу", color='secondary')],
            [get_button(label="Загрузить долг!", color='secondary')],[get_button(label="Загрузить на батл", color='secondary')], [get_button(label="Статистика дня и общая", color='secondary')]
        ]
    }
    keyboard_Admin = {
        "one_time": False,
        "buttons": [
            [get_button(label="Статистика дня и общая", color='secondary')],
            [get_button(label="Получить users", color='secondary'),get_button(label="Получить teams", color='secondary')],[get_button(label="Загрузить файл team", color='secondary'),get_button(label="Загрузить файл user", color='secondary')],
            [get_button(label="Начать челлендж", color='secondary'),get_button(label="Получить результаты челленджа", color='secondary')],
            [get_button(label="Очистить группу", color='negative')], [get_button(label="Назад", color='positive')]
        ]
    }
    keyboard = str(json.dumps(keyboard, ensure_ascii=False))
    keyboard_Leader = str(json.dumps(keyboard_Leader, ensure_ascii=False))
    keyboard_Admin = str(json.dumps(keyboard_Admin, ensure_ascii=False))


    def Leader(vk,keyboard_Leader):
        longpoll = VkBotLongPoll(vk, group_id)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if 'Статистика дня и общая' in event.object.message['text'] or '4' in event.object.message['text'] :
                    for i in get_Admin_statistic(event.object.message['peer_id']):
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': i,
                                                            'random_id': 0})
                    for i in Info_debt(event.object.message['peer_id']):
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': i,
                                                            'random_id': 0})

                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': Get_stat(),
                                                        'random_id': 0})

    def Admin_app_team(vk,name,both):#загружает команды
        longpoll = VkBotLongPoll(vk, group_id)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message['attachments'] and both == True:
                    if event.object.message['attachments'][0]['type'] == 'doc':  # новая база
                        url_team = event.object.message['attachments'][0]['doc']['url']
                        file_team = wget.download(url_team)
                        Save(file_team,name)
                        os.remove(file_team)
                        break
                elif len(event.object.message['attachments']) and both == False:
                    if event.object.message['attachments'][0]['type'] == 'doc':  # новая база
                        url_team = event.object.message['attachments'][0]['doc']['url']
                        file_team = wget.download(url_team)
                        Save(file_team, 'user.csv')
                        os.remove(file_team)
                    if event.object.message['attachments'][1]['type'] == 'doc':  # новая база
                        url_team = event.object.message['attachments'][1]['doc']['url']
                        file_team = wget.download(url_team)
                        Save(file_team, 'team.scv')
                        os.remove(file_team)
                else: break
    def Admin(vk,keyboard_Admin):
        longpoll = VkBotLongPoll(vk, group_id)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message['text'].lower() == 'Админ_начать':  # обратились к сообщению, образаемся к "тексту"
                    vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                                        'message': 'ok',
                                                        'random_id': 0, 'keyboard': keyboard_Admin})
                elif 'Статистика дня и общая' in event.object.message['text']: # НЕОБХОДИМО ПОЛУЧИТЬ КАКИЕ УЧАСТНИКИ И ИЗ КАКОЙ КОМАНДЫ. ИМЯ И ID  ID в формате "id@1233255"
                    for i in get_Admin_statistic():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': i,
                                                            'random_id': 0})
                    for i in Info_debt():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': i,
                                                            'random_id': 0})

                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': Get_stat(),
                                                        'random_id': 0})
                elif 'Загрузить файл user' in event.object.message['text']:
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': 'Загружай',
                                                        'random_id': 0})
                    Admin_app_team(vk, 'user.csv',True)
                elif 'Загрузить файл team' in event.object.message['text']:# ГОТОВО
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': 'Загружай',
                                                        'random_id': 0})
                    Admin_app_team(vk, 'user.csv',True)
                elif 'Получить users' in event.object.message['text']:#  ГОТОВО
                    upload_url = vk_photo.method('docs.getMessagesUploadServer',
                                                 {'type': 'doc',
                                                  'peer_id': event.object.message['peer_id']})['upload_url']

                    result = requests.post(upload_url, files={'file': open('users.csv', 'rb')}).json()
                    tmp = vk_photo.method('docs.save', {'file': result['file'], 'title': 'users'})['doc']
                    messages = vk_message.method('messages.send',
                                                 {'user_id': event.object.message['peer_id'],
                                                  'attachment': f'doc{tmp["owner_id"]}_{tmp["id"]}',
                                                  'random_id': 0,
                                                  'message': tmp['url']})
                elif 'Получить teams' in event.object.message['text']:  # доделать длля teams
                    upload_url = vk_photo.method('docs.getMessagesUploadServer',
                                                 {'type': 'doc',
                                                  'peer_id': event.object.message['peer_id']})['upload_url']

                    result = requests.post(upload_url, files={'file': open('users.csv', 'rb')}).json()
                    tmp = vk_photo.method('docs.save', {'file': result['file'], 'title': 'users'})['doc']
                    messages = vk_message.method('messages.send',
                                                 {'user_id': event.object.message['peer_id'],
                                                  'attachment': f'doc{tmp["owner_id"]}_{tmp["id"]}',
                                                  'random_id': 0,
                                                  'message': tmp['url']})
                elif 'Начать челлендж' in event.object.message['text']:# ГОТОВО
                    for i, g, k in get_Admin_statistic():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': f'{i} {g} {k}',
                                                            'random_id': 0})
                elif 'Получить результаты челленджа' in event.object.message['text']: #ГОТОВО НЕОБХОДИМО ПОЛУЧИТЬ КАКИЕ УЧАСТНИКИ И ИЗ КАКОЙ КОМАНДЫ. ИМЯ И ID
                    for i in chellenge():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': f'{i}',
                                                            'random_id': 0})
                elif 'Очистить группу' in event.object.message['text']: # НЕ ГОТОВО
                    items=vk_photo.method("groups.getMembers",{'group_id' : group_id})['items']
                    exclusion=(230810733,) #взять токен группы!!!!
                    for i in items:
                        if i in exclusion: continue
                        vk_photo.method("groups.removeUser",{'group_id' : group_id,'user_id':i})
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Группа очищена)",
                                                            'random_id': 0})
                elif 'Назад' in event.object.message['text']:
                    break
    def photo(body,user_id, url, group_id, album_id):
        file = wget.download(url)
        upload_url = vk_photo.method('photos.getUploadServer', {'group_id': group_id, 'album_id':

            album_id})['upload_url']
        info = requests.post(upload_url, files={'photo': open(file, 'rb')}).json()
        vk_photo.method('photos.save',
                        {'server': info['server'], 'photos_list': info['photos_list'], 'aid': info['aid'],
                         'hash': info['hash'], 'group_id': group_id, 'album_id': album_id, 'caption': body})
        os.remove(file)
    def daylik(vk,keyboard,album_id):
        longpoll = VkBotLongPoll(vk, group_id)
        flag2 = 0
        for event in longpoll.listen():
            if (hour_t() >= 1320) and (hour_t() < 1380):
                flag2 = 1
            elif hour_t() >= 1385:
                if flag2 != 0:

                    flag2 = 0
                    album_id = vk_photo.method('photos.createAlbum',
                                               {'title': str(day_t() + 1) + " День", 'group_id': group_id})['id']
            else:
                if flag2 != 0:
                    Counter_d()
                    Delete_us()
                    flag2 = 0
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message['attachments']:
                    if event.object.message['attachments'][0]['type'] == 'photo':  # photo
                        vk_message.method('messages.getConversations',
                                          {"peer_id": event.object.message['peer_id'],  # выведет ок если пришло фото
                                           'message': " Пришло фото!",
                                           'random_id': 0})
                        url = event.object.message['attachments'][0]['photo']['sizes'][5]['url']
                        messages = vk_message.method("messages.getConversations",
                                                     {'offset': 0, 'count': 20, 'filter': 'unread'})
                        file = wget.download(url)
                        id = event.object.message['peer_id']  # id отправителя
                        body = event.object.message['text']  # сам текст
                        photo(body,id, url, group_id, album_id)
                        if flag2 == 0: #до 22 часов
                            getpicture(event.object.message['peer_id'], 2, False)
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Отлично, работа принята!",
                                                                'random_id': 0})
                        if flag2 == 1:# медлу 22-00 и 23-00
                            getpicture(event.object.message['peer_id'], 1, False)
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Отлично, работа принята! Не опаздывай больше)",
                                                                'random_id': 0})
                        if flag2 == 2:#опоздал
                            getpicture(event.object.message['peer_id'], 0, False)
                        Counter()
                        os.remove(file)
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
                            url = event.object.message['attachments'][0]['photo']['sizes'][5]['url']
                            messages = vk_message.method("messages.getConversations",
                                                         {'offset': 0, 'count': 20, 'filter': 'unread'})
                            id = event.object.message['peer_id']  # id отправителя
                            body = event.object.message['text']  # сам текст
                            photo(body,id, url, group_id, album_id)
                            getpicture(event.object.message['peer_id'], 0.5, True)
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Отлично, долг принят!",
                                                                'random_id': 0})
                        Counter()
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
                            url = event.object.message['attachments'][0]['photo']['sizes'][5]['url']
                            messages = vk_message.method("messages.getConversations",
                                                    {'offset': 0, 'count': 20, 'filter': 'unread'})
                            id = event.object.message['peer_id']  # id отправителя
                            body = event.object.message['text']  # сам текст
                            album_Com_id = vk_photo.method('photos.createAlbum',# создает альбом для конкурсов
                                                       {'title': str(day_t() + 1) + " День. Конкурсы, ", 'group_id': group_id})['id']
                            photo(body,id, url, group_id, album_Com_id)
                            getpicture(event.object.message['peer_id'], 0, 2)
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Отлично, работа принята!",
                                                                'random_id': 0})
                break


    longpoll = VkBotLongPoll(vk_message, group_id) #событие, наблюдаем за некоторой событийной модель
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if user_in_base(event.object.message['peer_id']):
                if event.object.message['text'].lower() == 'начать':# обратились к сообщению, образаемся к "тексту"
                    a = vk_message.method('users.get', {'user_ids': event.object.message['peer_id']})
                    a = a[0]['first_name']
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': 'Привет, друг ' + str(a),
                                                        'random_id': 0})
                    vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                                'message': ' Нажми на кнопку или напиши необходимую команду,если кнопки не работают \n 0.Правила. \n 1. Загрузить работу.\n 2.Загрузить долг!.\n 3. Загрузить на конкурс',
                                                'random_id': 0, 'keyboard': keyboard})

                elif ("Правила" in event.object.message['text']) or ("0" in event.object.message['text']):  # НЕ ГОТОВО
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "https://vk.com/public191601892?w=wall-191601892_2", # тут правила
                                                            'random_id': 0})
                elif ("Загрузить работу" in event.object.message['text']) or ("1" in event.object.message['text']):## Как сделать так,чтобы бот передавал комментарий к рисунку вместе с рисуноком
                     if Data(event.object.message['peer_id'])==day_t():
                         vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                             'message': "Вы уже сдавали работу! Ждём вас завтра!",
                                                             'random_id': 0})
                     else:

                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                 'message': "Загружай!",
                                                 'random_id': 0})
                        daylik(vk_message,keyboard,album_id)
                        continue
                elif ("Загрузить долг!" in event.object.message['text']) or ("2" in event.object.message['text']):  # если нажать на кнопку, то проиходйет это
                    if Debt(event.object.message['peer_id']) <=0:
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Вы сдали все долги!",
                                                            'random_id': 0})
                    else:
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Загружайте долг",
                                                            'random_id': 0})
                        debt_daylik(vk_message,keyboard)
                elif ("Загрузить на батл" in event.object.message['text']) or ("3" in event.object.message['text']):

                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                 'message': "Загружай на конкурс",
                                                 'random_id': 0})
                    daylik_competition(vk_message,keyboard)



                elif event.object.message['text'].lower() == 'начать_админ': #админ
                    a = vk_message.method('users.get', {'user_ids': event.object.message['peer_id']})
                    a = a[0]['first_name']
                    vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                                        'message': 'Привет, администратор  '+str(a),
                                                        'random_id': 0, 'keyboard': keyboard_Admin})
                    Admin(vk_message,keyboard_Admin)

                elif event.object.message['text'].lower() == 'начать_староста': #староста БУДЕТ ЛИ ОН ПРИНИМАТЬ УЧАСТИЕ В ДЕЙЛИКАХ? НАДО ЛИ ДОБАВИТЬ СЮДА ФУНКЦЙИИ ИЛИ ВСЁ И ТАК БУДЕТ РАБОТАТЬ?
                    a = vk_message.method('users.get', {'user_ids': event.object.message['peer_id']})
                    a = a[0]['first_name']
                    vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                                        'message': 'Привет, администратор  '+str(a),
                                                        'random_id': 0, 'keyboard': keyboard_Leader})
                    Leader(vk_message,keyboard_Leader)

                else:

                    if event.object.message['attachments']:
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': ' Нажми на кнопку или напиши необходимую команду,если кнопки не работают \n 0.Правила. \n 1. Загрузить работу.\n 2.Загрузить долг!.\n 3. Загрузить на конкурс',
                                                            'random_id': 0})
                    else:
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Напечатай слово <начать>,чтобы приступить к работе",
                                                            'random_id': 0})
            else:
                vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                    'message': "Вы  были исключены из дейликов",
                                                    'random_id': 0})


