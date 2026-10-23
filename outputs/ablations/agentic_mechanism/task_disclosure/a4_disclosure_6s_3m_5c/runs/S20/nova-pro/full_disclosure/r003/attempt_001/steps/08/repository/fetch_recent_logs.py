import os
from datetime import datetime, timedelta
import requests

DATADOG_API_KEY = os.getenv('DATADOG_API_KEY')
DATADOG_APP_KEY = os.getenv('DATADOG_APP_KEY')
DATADOG_SITE = 'datadoghq.com'

def fetch_recent_logs(start_time: datetime, end_time: datetime, filter_field: str, filter_value: str):
    url = f'https://api.{DATADOG_SITE}/api/v2/logs'
    params = {
        'filter[query]': f'{filter_field}:{filter_value}',
        'start': int(start_time.timestamp()),
        'end': int(end_time.timestamp()),
    }
    headers = {
        'DD-API-KEY': DATADOG_API_KEY,
        'DD-APPLICATION-KEY': DATADOG_APP_KEY,
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    start_time = datetime.now() - timedelta(hours=1)
    end_time = datetime.now()
    logs = fetch_recent_logs(start_time, end_time, 'status', 'error')
    print(logs)