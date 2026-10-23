import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def log_text_safety(log_text):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = f'CustomLogs | where log_data contains "{log_text}" | summarize count()'
    response = client.query_workspace(os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID'), query)
    if response.status == LogsQueryStatus.SUCCESS:
        print('Safety check successful')
    else:
        print('Failed to perform safety check')