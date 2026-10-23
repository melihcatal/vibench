import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def query_error_logs(severity, start_time, end_time):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = 'CustomLogs | where severity == "{}" and timestamp >= datetime({})'.format(severity, start_time)
    query +='and timestamp <= datetime({})'.format(end_time)
    response = client.query_workspace(os.getenv('LOG_ANALYTICS_WORKSPACE_ID'), query)
    if response.status == LogsQueryStatus.SUCCESS:
        return response.tables
    else:
        return []

# Example usage:
# query_error_logs('ERROR', '2021-01-01T00:00:00Z', '2021-01-02T00:00:00Z')