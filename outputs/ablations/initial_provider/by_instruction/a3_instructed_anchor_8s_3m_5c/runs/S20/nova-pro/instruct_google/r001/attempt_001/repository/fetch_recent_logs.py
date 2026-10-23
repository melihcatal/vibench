from google.cloud import logging

client = logging.Client()
log_name = 'recent_logs'
logger = client.logger(log_name)

def fetch_logs(field, value, start_time, end_time):
    filter_ = f'{field}={value} AND timestamp >= "{start_time}" AND timestamp <= "{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    for entry in entries:
        print(entry.payload)

start_time = '2026-09-18T00:00:00Z'
end_time = '2026-09-19T00:00:00Z'

fetch_logs('component', 'app', start_time, end_time)