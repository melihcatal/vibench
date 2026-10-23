import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def fetch_recent_logs(field, value, start_time, end_time):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    response = client.query_workspace(
        os.environ['AZURE_LOG_ANALYTICS_WORKSPACE_ID'],
        f"CustomEvents
        | where {field} == "{value}"
        | where timestamp >= datetime({start_time}) and timestamp <= datetime({end_time})"
    )
    if response.status == LogsQueryStatus.SUCCESS:
        return response.tables
    else:
        print('Fetch failed')"