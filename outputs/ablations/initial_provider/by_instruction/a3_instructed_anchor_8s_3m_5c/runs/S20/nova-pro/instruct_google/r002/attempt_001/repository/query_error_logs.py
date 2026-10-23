import os
from google.cloud import logging

def query_error_logs(log_name, severity, start_time, end_time):
    client = logging.Client()
    logger = client.logger(log_name)
    filter_ = f'severity={severity} AND timestamp>="{start_time}" AND timestamp<="{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    for entry in entries:
        print(entry.payload)

if __name__ == '__main__':
    log_name = os.getenv('LOG_NAME', 'my_log')
    severity = 'ERROR'
    start_time = '2021-01-01T00:00:00Z'
    end_time = '2021-12-31T23:59:59Z'
    query_error_logs(log_name, severity, start_time, end_time)