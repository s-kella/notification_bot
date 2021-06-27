import requests
from dotenv import load_dotenv
import os
import time
import telegram

load_dotenv()
url = 'https://dvmn.org/api/long_polling/'
dvmn_token = os.getenv('DEVMAN_TOKEN')
tg_token = os.getenv('TG_TOKEN')
chat_id = os.getenv('TG_CHAT_ID')
header = {'Authorization': dvmn_token}
bot = telegram.Bot(token=tg_token)
timestamp = 0
while True:
    try:
        cur_time = time.time()
        if timestamp != 0:
            response = requests.get(url, headers=header, timeout=4, params=payload)
        else:
            response = requests.get(url, headers=header, timeout=4)
        response.raise_for_status()
        response = response.json()
        timestamp = response['new_attempts'][0]['timestamp']
        payload = {'timestamp': timestamp}
        lesson_title = response['new_attempts'][0]['lesson_title']
        lesson_url = f"dvmn.org{response['new_attempts'][0]['lesson_url']}"
        if response['new_attempts'][0]['is_negative']:
            is_negative = 'К сожалению, в работе есть ошибки :('
        else:
            is_negative = 'Всё супер, можно приступать к слеующей задаче!'
        bot.send_message(chat_id=chat_id,
                         text=f'Преподаватель проверил вашу работу "{lesson_title}"\n\n{is_negative}\n\n{lesson_url}.')
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectionError:
        if timestamp == 0:
            timestamp = cur_time
            payload = {'timestamp': timestamp}
        time.sleep(5)
