import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def write_structured_log(log_event):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = f"customEvents | extend event={log_event} | project event"
    response = client.query_workspace('your_workspace_id', query)
    if response.status == LogsQueryStatus.SUCCESS:
        print('Log written successfully')
    else:
        print('Log write failed')

log_event = "{'event_type': 'user_login', 'user_id': '12345'}"
write_structured_log(log_event)