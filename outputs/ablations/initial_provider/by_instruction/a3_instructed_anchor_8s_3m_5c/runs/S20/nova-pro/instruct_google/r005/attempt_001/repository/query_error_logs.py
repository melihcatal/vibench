import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('error_logs')

def query_logs(severity, start_time, end_time):
    filter_ = f'severity={severity} AND timestamp > "{start_time}" AND timestamp < "{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    for entry in entries:
        print(entry.payload)

if __name__ == '__main__':
    query_logs('ERROR', '2026-09-18T00:00:00Z', '2026-09-19T00:00:00Z')