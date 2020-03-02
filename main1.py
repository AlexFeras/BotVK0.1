import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json
import requests
import wget
from Base import getpicture, Counter, day_t, hour_t,Counter_d,Data,Debt,Save
from Admin_function import get_Admin_statistic,Get_stat,Info_debt
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
                    [get_button(label="Загрузить работу", color='secondary')],[get_button(label="Приветствие", color='positive'),get_button(label="Правила", color='positive')],
            [get_button(label="Загрузить долг!", color='positive')], [get_button(label="Загрузить на конкурс", color='positive')]
                    ]
    }

    keyboard_Leader = {
        "one_time": False,
        "buttons": [
            [get_button(label="Приветствие", color='positive'), get_button(label="Правила", color='positive')], [get_button(label="Загрузить работу", color='positive')],
            [get_button(label="Загрузить долг!", color='positive')],[get_button(label="Загрузить на конкурс", color='positive')], [get_button(label="Статистика дня и общая", color='positive')]
        ]
    }
    keyboard_Admin = {
        "one_time": False,
        "buttons": [
            [get_button(label="Статистика дня и общая", color='positive')],
            [get_button(label="Получить таблицы", color='positive')],[get_button(label="Загрузить файл team", color='positive'),get_button(label="Загрузить файл user", color='positive')],
            [get_button(label="Начать челлендж", color='negative'),get_button(label="получить результаты конкурса", color='negative')],
            [get_button(label="Очистить группу", color='negative')], [get_button(label="Назад", color='positive'), get_button(label="Начать челлендж", color='positive'),get_button(label="Получить результаты челленджа", color='positive')]
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
                    for i in get_Admin_statistic():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': i,
                                                            'random_id': 0})

    def Admin_app_team(vk):#загружает команды
        longpoll = VkBotLongPoll(vk, group_id)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message['attachments']:
                    if event.object.message['attachments'][0]['type'] == 'doc':  # новая база
                        url_team = event.object.message['attachments'][0]['doc']['url']
                        file_team = wget.download(url_team)
                        Save(file_team,'users.csv')
                        os.remove(file_team)
                        break
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
                    Admin_app_team(vk)
                elif 'Загрузить файл team' in event.object.message['text']:# НЕ ГОТОВО
                    for i, g, k in get_Admin_statistic():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': f'{i} {g} {k}',
                                                            'random_id': 0})
                elif 'Получить оба файла' in event.object.message['text']:# НЕ ГОТОВО
                    for i, g, k in get_Admin_statistic():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': f'{i} {g} {k}',
                                                            'random_id': 0})

                elif 'Начать челлендж' in event.object.message['text']:# НЕ ГОТОВО
                    for i, g, k in get_Admin_statistic():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': f'{i} {g} {k}',
                                                            'random_id': 0})
                elif 'Получить результаты челленджа' in event.object.message['text']: # НЕ ГОТОВО НЕОБХОДИМО ПОЛУЧИТЬ КАКИЕ УЧАСТНИКИ И ИЗ КАКОЙ КОМАНДЫ. ИМЯ И ID
                    for i, g, k in get_Admin_statistic():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': f'{i} {g} {k}',
                                                            'random_id': 0})
                elif 'Очистить группу' in event.object.message['text']:# НЕ ГОТОВО
                    for i, g, k in get_Admin_statistic():
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': f'{i} {g} {k}',
                                                            'random_id': 0})
                elif 'Назад' in event.object.message['text']:
                    break
    def photo(user_id, url, group_id, album_id):
        file = wget.download(url)
        upload_url = vk_photo.method('photos.getUploadServer', {'group_id': group_id, 'album_id':

            album_id})['upload_url']
        info = requests.post(upload_url, files={'photo': open(file, 'rb')}).json()
        vk_photo.method('photos.save',
                        {'server': info['server'], 'photos_list': info['photos_list'], 'aid': info['aid'],
                         'hash': info['hash'], 'group_id': group_id, 'album_id': album_id, 'caption': 'fsfs'})
        os.remove(file)
    def daylik(vk,keyboard):
        longpoll = VkBotLongPoll(vk, group_id)
        for event in longpoll.listen():
            flag2 = 0
            if (hour_t() >= 1320) and (hour_t() < 1380):
                flag2 = 1
            elif hour_t() >= 1380:
                if flag2 != 0:
                    flag2 = 0
                    album_id = vk_photo.method('photos.createAlbum',
                                               {'title': str(day_t() + 1) + " День", 'group_id': group_id})['id']
            else:
                if flag2 != 0:
                    Counter_d()
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
                        photo(id, url, group_id, album_id)
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
                        photo(id, url, group_id, album_id)
                        getpicture(event.object.message['peer_id'], 0.5, True)
                        vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                            'message': "Отлично, долг принят!",
                                                            'random_id': 0})
                        Counter()
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
                            photo(id, url, group_id, album_Com_id)
                            getpicture(event.object.message['peer_id'], 0, 2)
                            vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                                'message': "Отлично, работа принята!",
                                                                'random_id': 0})


    # если человек напишет что то кроме начать бот должен вывести, напиши именно это
    # если  придет изображение не нажав на кнопку или не отправив нужную цифру, тоже вывести оповещение. " Нажмите на кнопку или наберите цифру уважаемый
    longpoll = VkBotLongPoll(vk_message, group_id) #событие, наблюдаем за некоторой событийной модель
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.message['text'].lower() == 'начать':# обратились к сообщению, образаемся к "тексту"
                vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                            'message': ' Нажми на кнопку или напиши необходимую команду \n 0.Правила. \n 1. Загрузить работу.\n 2.Загрузить долг!.\n 3. Загрузить на конкурс',
                                            'random_id': 0, 'keyboard': keyboard})

            elif "Приветствие" in event.object.message['text']: # если нажать на кнопку, то проиходйет это
                a = vk_message.method('users.get', {'user_ids': event.object.message['peer_id']})
                a = a[0]['first_name']
                vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                        'message': 'Привет, друг '+str(a),
                                        'random_id': 0})
            elif "Правила" in event.object.message['text'] or "0" in event.object.message['text']:  # НЕ ГОТОВО
                if Debt(event.object.message['peer_id']) <=0:
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': "Тут будут правила", # должен брать текст из таблицы # Как его брать???
                                                        'random_id': 0})
            elif "Загрузить работу" in event.object.message['text'] or "1" in event.object.message['text']:## Как сделать так,чтобы бот передавал комментарий к рисунку вместе с рисуноком
                 if Data(event.object.message['peer_id'])==day_t():
                     vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                         'message': "Вы уже сдавали работу! Ждём вас завтра!",
                                                         'random_id': 0})
                 else:
                    daylik(vk_message,keyboard)
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                             'message': "Загружай!",
                                             'random_id': 0})
            elif "Загрузить долг!" in event.object.message['text'] or "2" in event.object.message['text']:  # если нажать на кнопку, то проиходйет это
                if Debt(event.object.message['peer_id']) <=0:
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': "Вы сдали все долги!",
                                                        'random_id': 0})
                else:
                    debt_daylik(vk_message,keyboard)
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': "Загружайте долг",
                                                        'random_id': 0})
            elif "Загрузить на конкурс" in event.object.message['text'] or "3" in event.object.message['text']:

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
                # vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                #                                     'message': 'Привет, администратор  ' + str(a),
                #                                     'random_id': 0, 'keyboard': keyboard})

            elif event.object.message['text'].lower() == 'начать_староста': #староста БУДЕТ ЛИ ОН ПРИНИМАТЬ УЧАСТИЕ В ДЕЙЛИКАХ? НАДО ЛИ ДОБАВИТЬ СЮДА ФУНКЦЙИИ ИЛИ ВСЁ И ТАК БУДЕТ РАБОТАТЬ?
                a = vk_message.method('users.get', {'user_ids': event.object.message['peer_id']})
                a = a[0]['first_name']
                vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                                    'message': 'Привет, администратор  '+str(a),
                                                    'random_id': 0, 'keyboard': keyboard_Leader})
                Leader(vk_message,keyboard_Leader)

                # изображения зачем то созраняет в корневую папку бота, как исправить?