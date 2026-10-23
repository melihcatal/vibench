import os
import json
import requests

# Azure Monitor Logs API endpoint
LOG_ANALYTICS_ENDPOINT = 'https://api.loganalytics.io/v1/workspaces/{workspaceId}/query'

# Azure Monitor Logs API headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + os.getenv('AZURE_MONITOR_LOGS_TOKEN')
}

def write_correlated_logs(logs):
    for log in logs:
        response = requests.post(LOG_ANALYTICS_ENDPOINT, headers=headers, data=json.dumps(log))
        if response.status_code == 200:
            print('Log written successfully')
        else:
            print('Failed to write log')

# Example correlated logs
correlated_logs = [
    {
        'time': '2026-09-21T12:00:00Z',
        'severity': 'INFO',
        'message': 'Request received',
        'correlationId': '12345'
    },
    {
        'time': '2026-09-21T12:00:01Z',
        'severity': 'INFO',
        'message': 'Request processed',
        'correlationId': '12345'
    }
]

write_correlated_logs(correlated_logs)