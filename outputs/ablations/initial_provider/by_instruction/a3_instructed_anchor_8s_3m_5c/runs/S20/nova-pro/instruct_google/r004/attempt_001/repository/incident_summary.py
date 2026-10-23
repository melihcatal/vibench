from google.cloud import logging
from datetime import datetime, timedelta

def summarize_error_logs(log_name):
    client = logging.Client()
    logger = client.logger(log_name)
    start_time = (datetime.utcnow() - timedelta(hours=1)).strftime('%%Y-%%m-%%dT%%H:%%M:%%SZ')
    end_time = datetime.utcnow().strftime('%%Y-%%m-%%dT%%H:%%M:%%SZ')
    filter_ = f'severity=ERROR AND timestamp>="{start_time}" AND timestamp<="{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    summary = {'total_errors': 0, 'error_messages': []}
    for entry in entries:
        summary['total_errors'] += 1
        summary['error_messages'].append(entry.payload['message'])
    return summary

if __name__ == '__main__':
    log_name = 'my_log'
    summary = summarize_error_logs(log_name)
    print(summary)