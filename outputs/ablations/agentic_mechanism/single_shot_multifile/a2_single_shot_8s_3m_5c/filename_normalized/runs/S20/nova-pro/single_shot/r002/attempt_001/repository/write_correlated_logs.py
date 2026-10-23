import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def write_correlated_logs(log_events):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    for log_event in log_events:
        query = f"customEvents | extend event={log_event} | project event"
        response = client.query_workspace('your_workspace_id', query)
        if response.status == LogsQueryStatus.SUCCESS:
            print('Log written successfully')
        else:
            print('Log write failed')

log_events = [{"event_type": 'user_login', "user_id": '12345', "correlation_id": 'abcde'}, {"event_type": 'user_logout', "user_id": '12345', "correlation_id": 'abcde'}]
write_correlated_logs(log_events)