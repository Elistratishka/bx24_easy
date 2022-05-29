import os
import datetime
import time
import requests
from dotenv import load_dotenv
from bitrix24 import *

load_dotenv()


def check_holidays():
    """Функция проверяет будет ли через 3 дня выходной день"""
    check_date = datetime.date.today() + datetime.timedelta(days=3)
    holidays = requests.get(f'https://isdayoff.ru/{check_date.strftime("%Y%m%d")}?cc=ru').json()
    return check_date, holidays


def add_task(check_date):
    """Функция получает дату и создает на её основе задачу в системе битрикс24
    Необходимо выдать права для работы с tasks своему вэбхуку"""
    bx24 = Bitrix24(os.getenv('WEBHOOK'))
    bx24.callMethod(
                 'tasks.task.add',
                 fields={'TITLE': 'Выходной/праздничный день',
                         'RESPONSIBLE_ID': 1,
                         'DEADLINE': f'{check_date}',
                         'DATE_START': f'{check_date}',
                         'CLOSED_DATE': f'{check_date + datetime.timedelta(days=1)}'},
            )


def main_loop():
    while True:
        check_date, holidays = check_holidays()
        if not holidays:
            add_task(check_date)
        time.sleep(86400)


if __name__ == '__main__':
    main_loop()
