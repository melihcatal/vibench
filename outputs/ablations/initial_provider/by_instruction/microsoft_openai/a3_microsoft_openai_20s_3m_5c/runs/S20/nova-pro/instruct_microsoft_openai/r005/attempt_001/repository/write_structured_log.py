import os
import json
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def write_structured_log(log_event):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = f"customEvents | extend timestamp = now(), name = '{log_event['name']}', value = {json.dumps(log_event['value'])}"
    response = client.query_workspace('<YOUR_WORKSPACE_ID>', query)
    if response.status == LogsQueryStatus.SUCCESS:
        print('Log written successfully')
    else:
        print('Log write failed')

if __name__ == '__main__':
    event = {'name': 'example_event', 'value': {'key': 'value'}}
    write_structured_log(event)