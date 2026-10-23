import os
from google.cloud import logging

def fetch_recent_logs(minutes: int = 60, field_filter: str = ''):
    """Fetches recent log entries filtered by field values and time range.

    Args:
        minutes (int): Time window in minutes (default 60).
        field_filter (str): Optional field filter e.g. 'severity=INFO'.
    """
    client = logging.Client()
    logger = client.logger('my-log')
    now = client.now()
    start = now - timedelta(minutes=minutes)
    filter_str = f'logName:projects/my-project/logs/my-log timestamp>={start} timestamp<={now}'
    if field_filter:
        filter_str += f' {field_filter}'
    logs = logger.list_entries(filter_=filter_str)
    for entry in logs:
        print({entry.timestamp.isoformat(): entry.payload})

# Example usage
if __name__ == '__main__':
    fetch_recent_logs(field_filter='severity=DEBUG')
