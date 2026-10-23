import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def summarize_error_logs(start_time, end_time):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    response = client.query_workspace(
        os.environ['AZURE_LOG_ANALYTICS_WORKSPACE_ID'],
        f"CustomEvents
        | where severity == 'Error'
        | where timestamp >= datetime({start_time}) and timestamp <= datetime({end_time})"
    )
    if response.status == LogsQueryStatus.SUCCESS:
        return response.tables
    else:
        print('Summary failed')"