import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json
import requests
import wget
from Base import getpicture, Counter, day_t, hour_t,Counter_d,Data,Debt,Save
import os

def get_button(label='but', color='red', payload=''):
    return {
        "action": {
            "type": 'text',
            'payload': payload,#идентификатор кнопки
            'label': label#то что написано на кнопке
        },
        "color": color
    }

if __name__ == "__main__":
    token =
    acess_token =
    group_id = 191601892
    album_id = 270167491
    vk_message = vk_api.VkApi(token=token)
    vk_photo = vk_api.VkApi(token=acess_token)
    v = '5.103'#версия приложения
    vk_message._auth_token()
    vk_message.get_api()
    vk_photo._auth_token()
    vk_photo.get_api()
    keyboard = { #создаем клавиатуру
        "one_time": False,
        "buttons": [
                    [get_button(label="Приветствие", color='positive')],[get_button(label="Сдать работу", color='positive')],
            [get_button(label="Сдать долг!", color='positive')]
                    ]
    }


    def photo(user_id, url, group_id, album_id):
        a = vk_photo.method("photos.getMessagesUploadServer")
        file = wget.download(url) # сохраняем файл
        b = requests.post(a['upload_url'], files={'photo': open(file, 'rb')}).json()
        c = vk_photo.method('photos.saveMessagesPhoto', {'photo': b['photo'],
                                                   'server': b['server'],
                                                   'hash': b['hash']})[0]
        vk_message.method("messages.send", {"peer_id": user_id, 'message': "Фото",
                                    "attachment": f'photo{c["owner_id"]}_{c["id"]}',
                                    'random_id': 0})
        # для работоспособности кода ниже - необходим standalone token
        upload_url = vk_photo.method('photos.getUploadServer',
                               {'group_id': group_id, 'album_id': album_id})['upload_url']
        info = requests.post(upload_url, files={'photo': open(file, 'rb')}).json()
        vk_photo.method('photos.save', {'server': info['server'],
                                  'photos_list': info['photos_list'],
                                  'aid': info['aid'],
                                  'hash': info['hash'], "album_id": album_id,
                                  'group_id': group_id})
        os.remove(file)

    keyboard = str(json.dumps(keyboard, ensure_ascii=False))# переводим в строковый тип, так как не может принимать словарь
    longpoll = VkBotLongPoll(vk_message, group_id) #событие, наблюдаем за некоторой событийной моделью
    flag=False
    flag1=False
    flag2=0
    for event in longpoll.listen():
        if (hour_t() >= 1320) and (hour_t()<1380):
            flag2=1
        elif hour_t()>=1243:
            flag2=2
            album_id = vk_photo.method('photos.createAlbum', {'title': str(day_t()) + " День", 'group_id': group_id})['id']
        else:
            if flag2!=0:
                Counter_d()
                flag2=0
        if event.type == VkBotEventType.MESSAGE_NEW:
            if flag == True:
                if event.object.message['attachments']:
                    if event.object.message['attachments'][0]['type'] == 'photo':  # photo
                        vk_message.method('messages.send',
                                  {"peer_id": event.object.message['peer_id'],  # выведет ок если пришло фото
                                   'attachment': 'photo-191601892_457239019',
                                   'random_id': 0})
                        url = event.object.message['attachments'][0]['photo']['sizes'][5]['url']
                        messages = vk_message.method("messages.getConversations",
                                             {'offset': 0, 'count': 20, 'filter': 'unread'})
                        id = event.object.message['peer_id']  # id отправителя
                        body = event.object.message['text']  # сам текст
                        photo(id, url, group_id, album_id)
                        if flag2 == 0: #до 22 часов
                            getpicture(event.object.message['peer_id'], 2, False)
                        if flag2 == 1:# медлу 22-00 и 23-00
                            getpicture(event.object.message['peer_id'], 1, False)
                        if flag2 == 2:#опоздал
                            getpicture(event.object.message['peer_id'], 3, False)
                        Counter()
                        flag = False
            if flag1 == True:
                if event.object.message['attachments']:
                    if event.object.message['attachments'][0]['type'] == 'photo':  # photo
                        vk_message.method('messages.send',
                                    {"peer_id": event.object.message['peer_id'],  # выведет ок если пришло фото
                                        'attachment': 'photo-191561475_457239022',
                                        'random_id': 0})
                        url = event.object.message['attachments'][0]['photo']['sizes'][5]['url']
                        messages = vk_message.method("messages.getConversations",
                                                {'offset': 0, 'count': 20, 'filter': 'unread'})
                        id = event.object.message['peer_id']  # id отправителя
                        body = event.object.message['text']  # сам текст
                        photo(id, url, group_id, album_id)
                        getpicture(event.object.message['peer_id'], 0.5, True)
                        Counter()
                        flag1 = False

            if event.object.message['text'].lower() == 'начать':# обратились к сообщению, образаемся к "тексту"
                vk_message.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                            'message': 'ok',
                                            'random_id': 0, 'keyboard': keyboard})

            elif "Приветствие" in event.object.message['text']: # если нажать на кнопку, то проиходйет это
                a = vk_message.method('users.get', {'user_ids': event.object.message['peer_id']})
                a = a[0]['first_name']
                vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                        'message': 'Привет, друг '+str(a),
                                        'random_id': 0})
            elif "Сдать работу" in event.object.message['text']:  # если нажать на кнопку, то проиходйет это
                 if Data(event.object.message['peer_id'])==day_t():
                     vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                         'message': "Вы уже сдавали работу! Ждём вас завтра!",
                                                         'random_id': 0})
                 else:
                    flag=True
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                             'message': "Загружай!",
                                             'random_id': 0})
            elif "Сдать долг!" in event.object.message['text']:  # если нажать на кнопку, то проиходйет это
                if Debt(event.object.message['peer_id']) <=0:
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                                        'message': "Вы сдали все долги!",
                                                        'random_id': 0})
                else:
                    flag1=True
                    vk_message.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                             'message': "Загружай долг!",
                                             'random_id': 0})
            elif "Admin" in event.object.message['text']:  # если нажать на кнопку, то проиходйет это
                if event.object.message['attachments'][0]['type'] == 'document':  #новая база
                    url_users = event.object.message['attachments'][0]['document']['url']
                    url_team  = event.object.message['attachments'][0]['document']['url']
                    a = vk_photo.method("photos.getMessagesUploadServer") # поулчить стандалон для фото и документов
                    file_users = wget.download(url_users)  # сохраняем файл
                    file_team = wget.download(url_team)
                    b = requests.post(a['upload_url'], files={'file': open(file, 'rb')}).json()
                    c = vk_photo.method('photos.save', {'document': b["file"],
                                                                     'server': b['server'],
                                                                     'hash': b['hash']})[0]
                    Save(file_users,file_team)
                    os.remove(file_users)
                    os.remove(file_team)





