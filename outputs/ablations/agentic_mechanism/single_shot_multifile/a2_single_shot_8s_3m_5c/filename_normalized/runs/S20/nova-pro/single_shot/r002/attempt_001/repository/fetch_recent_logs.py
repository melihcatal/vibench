import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def fetch_recent_logs():
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = 'customEvents | where timestamp > ago(1h) | project event'
    response = client.query_workspace('your_workspace_id', query)
    if response.status == LogsQueryStatus.SUCCESS:
        for row in response.tables[0].rows:
            print(row)
    else:
        print('Fetch failed')

fetch_recent_logs()