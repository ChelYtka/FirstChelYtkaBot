import requests
import time

API_URL = 'https://api.telegram.org/bot' # адрес обращения
f = open('token.txt')
BOT_TOKEN = f.readline()# токен бота
TEXT = 'Hello my dear CAT!!!' # текстовый ответ
ERROR_TEXT = 'Здесь должен быть кот('
MAX_COUNTER = 10

offset = -2 # -1 - возвращает последний апдейт, 0 - ничего не возвращает
counter = 0
chat_id: int # id чата

API_CAT_URL = 'https://api.thecatapi.com/v1/images/search'

while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет
    # делаем get-запрос и т.к. формат ответа известен, распарсим JSON с помощью метода json()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    # json() создаёт многоуровневый словарь

    if updates['result']: # проверяем, есть ли обновление

        for result in updates['result']:

            offset = result['update_id']
            chat_id = result['message']['from']['id']

            cat_response = requests.get(API_CAT_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']

                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')


    time.sleep(1)
    counter += 1