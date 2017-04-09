from pytz import timezone
from datetime import datetime, time

import requests


DEVMAN_API_URL = 'http://devman.org/api/challenges/solution_attempts'
MIDNIGHT = time(0, 0, 0)
NIGHT_END = time(5, 0, 0)


def load_attempts():
    params = {'page': 1}
    devman_data = requests.get(DEVMAN_API_URL, params).json()
    number_of_pages = int(devman_data['number_of_pages'])
    for page in range(1, number_of_pages + 1):
        params = {'page': page}
        devman_data = requests.get(DEVMAN_API_URL, params).json()
        print('Page {} was downloaded'.format(page))
        yield from devman_data['records']


def get_midnighters(records):
    midnighters_set = set()
    for record in records:
        if (record['timestamp'] and record['timezone']) is None:
            print('Warning: timestamp or timezone is None')
            continue
        local_date_time = datetime.fromtimestamp(float(record['timestamp'],),
                                                 tz=timezone(record['timezone']))
        user_time = local_date_time.time()
        if MIDNIGH < user_time < NIGHT_END:
            midnighters_set.add(record['username'])
    return midnighters_set


if __name__ == '__main__':
    records = load_attempts()
    midnighters = get_midnighters(records)
    print('\nMidnighters:')
    for midnighter in midnighters:
        print(midnighter)
