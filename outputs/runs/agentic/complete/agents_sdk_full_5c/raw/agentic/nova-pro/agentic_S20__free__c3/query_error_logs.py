import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)

log_query = 'AppTraces | where severity == "error" | summarize count() by bin(timestamp, 1h)'
response = client.query_workspace(os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID'), log_query)
if response.status == LogsQueryStatus.SUCCESS:
    for row in response.tables[0].rows:
        print(row)