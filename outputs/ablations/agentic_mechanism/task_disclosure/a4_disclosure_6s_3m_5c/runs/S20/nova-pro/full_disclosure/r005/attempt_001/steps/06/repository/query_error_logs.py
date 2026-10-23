import os
from datadog import initialize, api

options = {
    'api_key': os.getenv('DATADOG_API_KEY'),
    'app_key': os.getenv('DATADOG_APP_KEY')
}

initialize(**options)

def query_error_logs(severity, start_time, end_time):
    query = f'status:error severity:{severity}'
    logs = api.Logs.query(query=query, start=start_time, end=end_time)
    return logs

if __name__ == '__main__':\n    severity = 'error'\n    start_time = 1609459200 # Example start time in UNIX timestamp\n    end_time = 1609545600 # Example end time in UNIX timestamp\n    logs = query_error_logs(severity, start_time, end_time)\n    print(logs)