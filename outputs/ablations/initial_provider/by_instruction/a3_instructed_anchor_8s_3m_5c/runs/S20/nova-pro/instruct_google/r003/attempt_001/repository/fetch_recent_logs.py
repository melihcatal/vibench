from google.cloud import logging

def fetch_recent_logs(log_name, field_name, field_value, start_time, end_time):
    client = logging.Client()
    logger = client.logger(log_name)
    filter_ = f'{field_name}={field_value} AND timestamp>="{start_time}" AND timestamp<="{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    for entry in entries:
        print(entry.payload)

if __name__ == '__main__':
    log_name = 'my_log'
    field_name = 'correlation_id'
    field_value = '12345'
    start_time = '2026-09-19T00:00:00Z'
    end_time = '2026-09-19T23:59:59Z'
    fetch_recent_logs(log_name, field_name, field_value, start_time, end_time)