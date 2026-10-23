import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def write_structured_log(log_data):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = f'CustomLogs | extend log_data={log_data} | summarize count()'
    response = client.query_workspace(os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID'), query)
    if response.status == LogsQueryStatus.SUCCESS:
        print('Log written successfully')
    else:
        print('Failed to write log')