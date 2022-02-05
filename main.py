import requests
from dotenv import load_dotenv
import os
import time
import telegram
import logging

logger = logging.getLogger('Logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    url = 'https://dvmn.org/api/long_polling/'
    dvmn_token = os.getenv('DEVMAN_TOKEN')
    tg_notif_token = os.getenv('TG_NOTIF_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    header = {'Authorization': dvmn_token}
    notification_bot = telegram.Bot(token=tg_notif_token)

    tg_log_token = os.getenv('TG_LOG_TOKEN')
    log_bot = telegram.Bot(token=tg_log_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))
    logger.info('The bot is runnning')

    timestamp = time.time()
    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(url, headers=header, timeout=60, params=payload)
            response.raise_for_status()
            response_data = response.json()
            if response_data['status'] == 'found':
                attempt_info = response_data['new_attempts'][0]
                timestamp = response_data['last_attempt_timestamp']
                lesson_title = attempt_info['lesson_title']
                lesson_url = f"{attempt_info['lesson_url']}"
                if attempt_info['is_negative']:
                    is_negative = 'К сожалению, в работе есть ошибки :('
                else:
                    is_negative = 'Всё супер, можно приступать к следующей задаче!'
                notification_bot.send_message(chat_id=chat_id,
                                 text=f'Преподаватель проверил вашу работу "{lesson_title}".\n\n{is_negative}\n\n{lesson_url}')
            else:
                timestamp = response_data['timestamp_to_request']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(5)
        except Exception as e:
            logger.exception(f'Bot crashed with the error: {e}\n\n')


if __name__ == '__main__':
    main()
