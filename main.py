import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json
import requests
import wget #скачать её
#from Counter import *


def get_button(label='but', color='red', payload=''):
    return {
        "action": {
            "type": 'text',
            'payload': payload,#идентификатор кнопки
            'label': label#то что написано на кнопке
        },
        "color": color
    }
# k=day_t() модуль работает, но бот тогда не работает)))
# print(k)

if __name__ == "__main__":
    token = 'c713225662ae3c53a7f659faa894c5bfbf940208aaf60148ba34bf29289c54f82d2f3cd92cec8e466aa4a'
    access_token = 'd156760681eab18bcee0acc3de2185eed9f45e17456967d3c5c0d81a4b94b22473c0173759fc97178f395'
    group_id = 191561475
    album_id = 269997215
    vk = vk_api.VkApi(token=token)
    v = '5.103'#версия приложения
    vk._auth_token()
    vk.get_api()
    keyboard = { #создаем клавиатуру
        "one_time": False,
        "buttons": [
                    [get_button(label="Приветствие", color='positive')],
                    [get_button(label="Данные о боте", color='positive')],
                    [get_button(label="Кнопка", color='positive')]
                    ]
    }


    def photo(user_id, url, group_id, album_id, token):
        a = vk.method("photos.getMessagesUploadServer")
        file = wget.download(url)  # сохраняем файл
        b = requests.post(a['upload_url'], files={'photo': open(file, 'rb')}).json()
        c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'],
                                                   'server': b['server'],
                                                   'hash': b['hash']})[0]
        vk.method("messages.send", {"peer_id": user_id, 'message': "Фото",
                                    "attachment": f'photo{c["owner_id"]}_{c["id"]}',
                                    'random_id': 0})
        # для работоспособности кода ниже - необходим standalone token
        upload_url = vk.method('photos.getUploadServer',
                               {'access_token': access_token, 'group_id': group_id, 'album_id': album_id})['upload_url']
        info = requests.post(upload_url, files={'photo': open(file, 'rb')}).json()
        vk.method('photos.save', {'server': info['server'],
                                  'photos_list': info['photos_list'],
                                  'aid': info['aid'],
                                  'hash': info['hash'],
                                  'group_id': group_id})

    keyboard = str(json.dumps(keyboard, ensure_ascii=False))# переводим в строковый тип, так как не может принимать словарь
    longpoll = VkBotLongPoll(vk, group_id) #событие, наблюдаем за некоторой событийной моделью
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.message['text'].lower() == 'начать':# обратились к сообщению, образаемся к "тексту"
                vk.method("messages.send", {"peer_id": event.object.message['peer_id'],
                                            'message': 'ok',
                                            'random_id': 0, 'keyboard': keyboard})

            elif "Приветствие" in event.object.message['text']: # если нажать на кнопку, то проиходйет это
                a = vk.method('users.get', {'user_ids': event.object.message['peer_id']})
                a = a[0]['first_name']
                vk.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                        'message': 'Привет, друг '+str(a),
                                        'random_id': 0})
            elif "Кнопка" in event.object.message['text']:  # если нажать на кнопку, то проиходйет это
                 vk.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                             'message': "Кнопка",
                                             'random_id': 0})

            elif "Данные о боте" in event.object.message['text']:  # если нажать на кнопку, то проиходйет это
                 vk.method('messages.send', {"peer_id": event.object.message['peer_id'],
                                             'message': 'Бот для дейликов,версия 0.1. Предназначен для подсчета баллов людей участвующих в дейликах и конкурсах группы.!',
                                             'random_id': 0})
            elif event.object.message['attachments'][0]['type'] == 'photo': #photo
                 vk.method('messages.send', {"peer_id": event.object.message['peer_id'],#выведет ок если пришло фото
                                            'attachment': 'photo-191561475_457239022',
                                            'random_id': 0})

                 #-------код что ниже, при запуске вырубает бота. Идёт ошибка
                 url = event.object.message['attachments'][0]['photo']['sizes'][5]['url']
                 messages = vk.method("messages.getConversations", {'offset': 0, 'count': 20, 'filter':'unread'})
                 id = event.object.message['peer_id'] #id отправителя
                 body = event.object.message['text']# сам текст
                 #photo(id, url, group_id, album_id, 269997215)





