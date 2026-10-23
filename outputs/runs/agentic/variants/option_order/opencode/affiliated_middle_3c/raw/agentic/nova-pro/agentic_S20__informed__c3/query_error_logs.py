import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential


def query_error_logs(severity, start_time, end_time):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = f"search in (Traces) severity={severity} | where timestamp >= {start_time} and timestamp <= {end_time}"
    response = client.query_workspace(
        os.environ["AZURE_LOG_ANALYTICS_WORKSPACE_ID"], query
    )
    if response.status == LogsQueryStatus.SUCCESS:
        return response.tables
    else:
        print("Failed to query error logs")
