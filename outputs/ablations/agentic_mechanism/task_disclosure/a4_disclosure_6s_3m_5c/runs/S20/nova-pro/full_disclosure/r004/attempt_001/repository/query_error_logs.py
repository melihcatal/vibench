from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def query_error_logs(workspace_id, query, severity, start_time, end_time):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    response = client.query_workspace(workspace_id, query, start_time=start_time, end_time=end_time)

    if response.status == LogsQueryStatus.SUCCESS:
        return response.tables
    else:
        raise Exception(f"Query failed with status: {response.status}")

# Example usage:
# query_error_logs('my-workspace-id', 'AzureActivity | where CategoryValue == "error" and SeverityLevel == "{severity}" | summarize count() by bin(TimeGenerated, 1h)', 'Error', '2026-09-19T00:00:00Z', '2026-09-19T23:59:59Z')