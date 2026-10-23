import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def incident_summary():
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = 'CustomLogs | where severity == "error" | summarize count()'
    response = client.query_workspace(os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID'), query)
    if response.status == LogsQueryStatus.SUCCESS:
        print('Summary generated successfully')
    else:
        print('Failed to generate summary')