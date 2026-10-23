import os
from datadog import initialize, api

options = {
    'api_key': os.getenv('DATADOG_API_KEY'),
    'app_key': os.getenv('DATADOG_APP_KEY')
}

initialize(**options)

def fetch_recent_logs(start, end, query):
    response = api.Log.search(
        start=start,
        end=end,
        query=query
    )
    return response

if __name__ == '__main__':
    start = 1609459200  # Example start time (Unix timestamp)
    end = 1609545600    # Example end time (Unix timestamp)
    query = 'source:python'  # Example query
    logs = fetch_recent_logs(start, end, query)
    print(logs)