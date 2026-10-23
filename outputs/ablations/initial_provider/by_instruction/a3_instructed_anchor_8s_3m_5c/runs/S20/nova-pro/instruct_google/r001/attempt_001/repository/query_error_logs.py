from google.cloud import logging

client = logging.Client()
log_name = 'error_logs'
logger = client.logger(log_name)

def query_logs(severity, start_time, end_time):
    filter_ = f'severity={severity} AND timestamp >= "{start_time}" AND timestamp <= "{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    for entry in entries:
        print(entry.payload)

start_time = '2026-09-18T00:00:00Z'
end_time = '2026-09-19T00:00:00Z'

query_logs('ERROR', start_time, end_time)