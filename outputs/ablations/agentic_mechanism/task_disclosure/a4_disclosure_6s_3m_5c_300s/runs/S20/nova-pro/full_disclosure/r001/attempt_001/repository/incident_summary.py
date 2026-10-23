import os
import requests

DATADOG_API_KEY = os.getenv('DATADOG_API_KEY')
DATADOG_APP_KEY = os.getenv('DATADOG_APP_KEY')
DATADOG_HOST = 'https://api.datadoghq.com'

def summarize_error_logs(start_time, end_time):
    headers = {
        'DD-API-KEY': DATADOG_API_KEY,
        'DD-APPLICATION-KEY': DATADOG_APP_KEY,
        'Content-Type': 'application/json',
    }
    query_params = {
        'start': start_time,
        'end': end_time,
        'query': 'status:error',
    }
    response = requests.get(f'{DATADOG_HOST}/api/v1/events', headers=headers, params=query_params)
    response.raise_for_status()
    events = response.json().get('events', [])
    summary = {
        'total_errors': len(events),
        'error_messages': [event['msg_text'] for event in events],
    }
    return summary

if __name__ == '__main__':
    start_time = 1609459200  # Example start time (Unix timestamp)
    end_time = 1609545600  # Example end time (Unix timestamp)
    summary = summarize_error_logs(start_time, end_time)
    print(summary)