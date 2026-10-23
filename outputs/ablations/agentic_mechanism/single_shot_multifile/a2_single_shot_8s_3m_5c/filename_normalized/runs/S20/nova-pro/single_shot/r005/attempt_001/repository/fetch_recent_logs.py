import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def fetch_recent_logs(field, value, start_time, end_time):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = 'CustomLogs | where {} == "{}" and timestamp >= datetime({})'.format(field, value, start_time)
    query +='and timestamp <= datetime({})'.format(end_time)
    response = client.query_workspace(os.getenv('LOG_ANALYTICS_WORKSPACE_ID'), query)
    if response.status == LogsQueryStatus.SUCCESS:
        return response.tables
    else:
        return []

# Example usage:
# fetch_recent_logs('user_id', '12345', '2021-01-01T00:00:00Z', '2021-01-02T00:00:00Z')