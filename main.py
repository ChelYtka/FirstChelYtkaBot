import requests
import time

API_URL = 'https://api.telegram.org/bot' # адрес обращения
f = open('token.txt')
BOT_TOKEN = f.readline()# токен бота
TEXT = 'Hello world!!!' # текстовый ответ
MAX_COUNTER = 10

offset = -2 # -1 - возвращает последний апдейт, 0 - ничего не возвращает
counter = 0
chat_id: int # id чата

while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет
    # делаем get-запрос и т.к. формат ответа известен, распарсим JSON с помощью метода json()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    # json() создаёт многоуровневый словарь

    if updates['result']: # проверяем, есть ли обновление
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')

    time.sleep(1)
    counter += 1