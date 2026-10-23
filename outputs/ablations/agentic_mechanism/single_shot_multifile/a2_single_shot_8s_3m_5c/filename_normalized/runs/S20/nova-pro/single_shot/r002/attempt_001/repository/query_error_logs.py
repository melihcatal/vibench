import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def query_error_logs():
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = 'exceptions | where severityLevel == 3 | summarize count() by bin(timestamp, 1h)'
    response = client.query_workspace('your_workspace_id', query)
    if response.status == LogsQueryStatus.SUCCESS:
        for row in response.tables[0].rows:
            print(row)
    else:
        print('Query failed')

query_error_logs()