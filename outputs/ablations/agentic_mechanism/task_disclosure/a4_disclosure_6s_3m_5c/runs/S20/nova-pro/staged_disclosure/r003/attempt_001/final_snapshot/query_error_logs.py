import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def query_error_logs(workspace_id, query, start_time, end_time):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    response = client.query_workspace(workspace_id, query, start_time, end_time)

    if response.status == LogsQueryStatus.SUCCESS:
        for row in response.tables[0].rows:
            print(row)
    else:
        print(f"Query failed (status: {response.status})")

if __name__ == "__main__":
    workspace_id = os.getenv('AZURE_MONITOR_WORKSPACE_ID')
    query = "AppTraces | where severityLevel == 'Error' | summarize count() by bin(timestamp, 1h)"
    start_time = "2026-09-01T00:00:00Z"
    end_time = "2026-09-19T00:00:00Z"
    query_error_logs(workspace_id, query, start_time, end_time)
