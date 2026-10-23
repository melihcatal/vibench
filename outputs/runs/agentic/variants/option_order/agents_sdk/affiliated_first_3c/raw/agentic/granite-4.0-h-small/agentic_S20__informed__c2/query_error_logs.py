import os, json, requests

# Provider: Azure Monitor Logs (REST)
AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
RESOURCE_GROUP = 'my-resource-group'
WORKSPACE_NAME = 'my-log-analytics'

# Obtain OAuth token
import requests, time

def get_oauth_token():
    url = f'https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': AZURE_CLIENT_ID,
        'client_secret': AZURE_CLIENT_SECRET,
        'resource': 'https://management.azure.com/'
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()['access_token']

token = get_oauth_token()
auth_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

BASE_URL = f'https://management.azure.com/subscriptions/{AZURE_TENANT_ID}/resourcegroups/{RESOURCE_GROUP}/providers/Microsoft.OperationalInsights/workspaces/{WORKSPACE_NAME}/query?api-version=2021-12-01-preview'

def query_error_logs(severity='Error', start_time='now-15m'):
    """Query recent error log entries in Azure Monitor (Log Analytics)"""
    query = f"{WORKSPACE_NAME}_CL | where severity_level_s == '{severity}' and TimeGenerated > ago({start_time})"
    payload = {
        'query': query,
        'timespan': 'PT15M'
    }
    resp = requests.post(BASE_URL, headers=auth_headers, json=payload, timeout=20)
    resp.raise_for_status()
    result = resp.json()
    tables = result.get('tables', [])
    if not tables:
        return []
    rows = tables[0].get('rows', [])
    return rows

if __name__ == '__main__':
    logs = query_error_logs()
    print(json.dumps(logs, indent=2))
