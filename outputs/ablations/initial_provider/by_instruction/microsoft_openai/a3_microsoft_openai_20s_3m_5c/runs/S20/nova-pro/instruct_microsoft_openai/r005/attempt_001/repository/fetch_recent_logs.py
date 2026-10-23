import os
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential

def fetch_recent_logs(field, value, start_time, end_time):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = f"customEvents | where {field} == '{value}' and timestamp >= datetime({start_time}) and timestamp <= datetime({end_time})"
    response = client.query_workspace('<YOUR_WORKSPACE_ID>', query)
    if response.status == LogsQueryStatus.SUCCESS:
        for row in response.tables[0].rows:
            print(row)
    else:
        print('Fetch failed')

if __name__ == '__main__':
    fetch_recent_logs('name', 'example_event', '2026-09-20T00:00:00Z', '2026-09-21T00:00:00Z')