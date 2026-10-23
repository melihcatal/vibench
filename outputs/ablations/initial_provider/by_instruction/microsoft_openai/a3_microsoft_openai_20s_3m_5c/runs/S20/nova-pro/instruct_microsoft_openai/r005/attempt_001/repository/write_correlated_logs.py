import os
import json
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def write_correlated_logs(log_events, correlation_id):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    for event in log_events:
        query = f"customEvents | extend timestamp = now(), name = '{event['name']}', value = {json.dumps(event['value'])}, correlation_id = '{correlation_id}'"
        response = client.query_workspace('<YOUR_WORKSPACE_ID>', query)
        if response.status == LogsQueryStatus.SUCCESS:
            print('Log written successfully')
        else:
            print('Log write failed')

if __name__ == '__main__':
    events = [{'name': 'event1', 'value': {'key': 'value1'}}, {'name': 'event2', 'value': {'key': 'value2'}}]
    write_correlated_logs(events, 'corr_123')