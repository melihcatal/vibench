import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('recent_logs')

def fetch_logs(field, value, start_time, end_time):
    filter_ = f'{field}={value} AND timestamp > "{start_time}" AND timestamp < "{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    for entry in entries:
        print(entry.payload)

if __name__ == '__main__':
    fetch_logs('component', 'app', '2026-09-18T00:00:00Z', '2026-09-19T00:00:00Z')