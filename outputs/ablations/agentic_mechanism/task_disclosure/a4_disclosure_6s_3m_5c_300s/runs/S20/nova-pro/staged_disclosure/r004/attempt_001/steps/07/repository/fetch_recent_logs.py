import os
from datadog import initialize, api

options = {
    'api_key': os.getenv('DATADOG_API_KEY'),
    'app_key': os.getenv('DATADOG_APP_KEY')
}

initialize(**options)

def fetch_recent_logs(query, start, end):
    logs = api.Logs.search(query=query, start=start, end=end)
    return logs

if __name__ == '__main__':
    query = 'source:python'
    start = 1609459200  # Example start time
    end = 1609545600  # Example end time
    logs = fetch_recent_logs(query, start, end)
    print(logs)