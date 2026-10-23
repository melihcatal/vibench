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

def write_log(log_data):
    response = requests.post(LOG_ANALYTICS_ENDPOINT, headers=headers, data=json.dumps(log_data))
    if response.status_code == 200:
        print('Log written successfully')
    else:
        print('Failed to write log')

# Example log data
log_data = {
    'time': '2026-09-21T12:00:00Z',
    'severity': 'INFO',
    'message': 'Application started successfully'
}

write_log(log_data)