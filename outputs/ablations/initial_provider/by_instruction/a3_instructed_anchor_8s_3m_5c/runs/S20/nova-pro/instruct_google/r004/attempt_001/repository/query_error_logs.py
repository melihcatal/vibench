from google.cloud import logging
from datetime import datetime, timedelta

def query_error_logs(log_name, severity, start_time, end_time):
    client = logging.Client()
    logger = client.logger(log_name)
    filter_ = f'severity={severity} AND timestamp>="{start_time}" AND timestamp<="{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    for entry in entries:
        print(entry.payload)

if __name__ == '__main__':
    log_name = 'my_log'
    severity = 'ERROR'
    start_time = (datetime.utcnow() - timedelta(hours=1)).strftime('%%Y-%%m-%%dT%%H:%%M:%%SZ')
    end_time = datetime.utcnow().strftime('%%Y-%%m-%%dT%%H:%%M:%%SZ')
    query_error_logs(log_name, severity, start_time, end_time)