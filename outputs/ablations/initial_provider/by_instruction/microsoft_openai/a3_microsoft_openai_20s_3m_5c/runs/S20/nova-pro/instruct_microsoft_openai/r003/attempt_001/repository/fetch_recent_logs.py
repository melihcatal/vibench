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

def fetch_recent_logs(field, value, start_time, end_time):
    query = f'\n    | where {field} == "{value}" and time >= datetime({start_time}) and time <= datetime({end_time}) \n'
    response = requests.post(LOG_ANALYTICS_ENDPOINT, headers=headers, data=json.dumps({'query': query}))
    if response.status_code == 200:
        print('Logs fetched successfully')
    else:
        print('Failed to fetch logs')

# Example fetch parameters
field = 'severity'
value = 'INFO'
start_time = '2026-09-20T00:00:00Z'
end_time = '2026-09-21T00:00:00Z'

fetch_recent_logs(field, value, start_time, end_time)