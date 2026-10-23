import os
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential

def summarize_error_logs(severity, start_time, end_time):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = f"exceptions | where severity == '{severity}' and timestamp >= datetime({start_time}) and timestamp <= datetime({end_time}) | summarize count() by problemId"
    response = client.query_workspace('<YOUR_WORKSPACE_ID>', query)
    if response.status == LogsQueryStatus.SUCCESS:
        for row in response.tables[0].rows:
            print(row)
    else:
        print('Summarization failed')

if __name__ == '__main__':
    summarize_error_logs('error', '2026-09-20T00:00:00Z', '2026-09-21T00:00:00Z')