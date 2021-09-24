import requests
from dotenv import load_dotenv
import os
import time
import telegram


def main():
    load_dotenv()
    url = 'https://dvmn.org/api/long_polling/'
    dvmn_token = os.getenv('DEVMAN_TOKEN')
    tg_token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    header = {'Authorization': dvmn_token}
    bot = telegram.Bot(token=tg_token)
    timestamp = time.time()
    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(url, headers=header, timeout=4, params=payload)
            response.raise_for_status()
            response_data = response.json()
            if response_data['status'] == 'found':
                attempt_info = response_data['new_attempts'][0]
                timestamp = response_data['last_attempt_timestamp']
                lesson_title = attempt_info['lesson_title']
                lesson_url = f"dvmn.org{attempt_info['lesson_url']}"
                if attempt_info['is_negative']:
                    is_negative = 'К сожалению, в работе есть ошибки :('
                else:
                    is_negative = 'Всё супер, можно приступать к слеующей задаче!'
                bot.send_message(chat_id=chat_id,
                                 text=f'Преподаватель проверил вашу работу "{lesson_title}".\n\n{is_negative}\n\n{lesson_url}')
            else:
                timestamp = response_data['timestamp_to_request']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(5)


if __name__ == '__main__':
    main()
