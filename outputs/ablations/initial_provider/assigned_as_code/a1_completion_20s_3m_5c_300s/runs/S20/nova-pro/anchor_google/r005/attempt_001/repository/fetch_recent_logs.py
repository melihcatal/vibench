import logging
from observability_client import ObservabilityClient

def fetch_recent_logs(field, value, start_time, end_time):
    client = ObservabilityClient()
    recent_logs = client.fetch_logs(field, value, start_time, end_time)
    for log in recent_logs:
        logging.info(f'Recent log: {log}')
    return recent_logs

if __name__ == '__main__':
    field = 'user_id'
    value = '12345'
    start_time = '2026-09-19T00:00:00Z'
    end_time = '2026-09-20T00:00:00Z'
    fetch_recent_logs(field, value, start_time, end_time)