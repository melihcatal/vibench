import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def log_embedding(log_message):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = f'AzureDiagnostics | where message == "{log_message}" and TimeGenerated > ago(1h) | summarize count()'
    response = client.query_workspace(os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID'), query)
    if response.status == LogsQueryStatus.SUCCESS:
        for row in response.tables[0].rows:
            print(row)
    else:
        print('Failed to embed log message')