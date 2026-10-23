import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def log_message_translate(log_text):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = f'CustomLogs | where log_data contains "{log_text}" | summarize count()'
    response = client.query_workspace(os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID'), query)
    if response.status == LogsQueryStatus.SUCCESS:
        print('Translation successful')
    else:
        print('Failed to translate log message')