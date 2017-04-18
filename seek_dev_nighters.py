from datetime import datetime, time

from pytz import timezone
import requests


DEVMAN_API_URL = 'http://devman.org/api/challenges/solution_attempts'
MIDNIGHT = 0
NIGHT_END = 5


def load_attempts():
    number_of_pages = None
    if number_of_pages is None:
        params = {'page': 1}
        devman_data = requests.get(DEVMAN_API_URL, params).json()
        number_of_pages = int(devman_data['number_of_pages'])
        yield from devman_data['records']
    
    for page in range(2, number_of_pages + 1):
        params = {'page': page}
        devman_data = requests.get(DEVMAN_API_URL, params).json()
        yield from devman_data['records']


def get_midnighters(records):
    midnighters_set = set()
    warnings = []
    for record in records:
        if record['timestamp'] is None:
            warnings.append('User: {}. Warning: timestamp is None'.format(record['username']))
            continue
        if record['timezone'] is None:
            warnings.append('User: {}. Warning: timezone is None'.format(record['username']))
            continue
        local_date_time = datetime.fromtimestamp(float(record['timestamp'],),
                                                 tz=timezone(record['timezone']))
        user_time = local_date_time.time()
        if MIDNIGHT < user_time.hour < NIGHT_END:
            midnighters_set.add(record['username'])
    if warnings == []:
        warnings = ['Everything is ok: no empty timestamp and timezone']
    return midnighters_set, warnings


if __name__ == '__main__':
    records = load_attempts()
    midnighters, warnings = get_midnighters(records)
    print('\nWarnings:')
    for warning in warnings:
        print(warning)
    
    print('\nMidnighters:')
    for midnighter in midnighters:
        print(midnighter)
