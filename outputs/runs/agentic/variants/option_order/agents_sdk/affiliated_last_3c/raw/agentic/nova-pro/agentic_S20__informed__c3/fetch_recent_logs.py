import os
from azure.monitor.query import LogsQueryClient, LogsQueryOptions

client = LogsQueryClient(credential=os.getenv('AZURE_MONITOR_LOGS_CREDENTIALS'))

def fetch_recent_logs():
    query = 'AzureDiagnostics | where TimeGenerated > ago(1h)'
    response = client.query_workspace(workspace_id=os.getenv('AZURE_MONITOR_LOGS_WORKSPACE_ID'), query=query, options=LogsQueryOptions(timespan='PT1H'))
    return response.tables[0].rows