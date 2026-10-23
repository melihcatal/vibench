import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def write_correlated_logs(log_events, correlation_id):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    for log_event in log_events:
        response = client.query_workspace(
            os.environ['AZURE_LOG_ANALYTICS_WORKSPACE_ID'],
            f"CustomEvents | extend timestamp = now(), log_event = "{log_event}", correlation_id = "{correlation_id}" | project-rename event_data = log_event"
        )
        if response.status == LogsQueryStatus.SUCCESS:
            print('Log written successfully')
        else:
            print('Log write failed')"