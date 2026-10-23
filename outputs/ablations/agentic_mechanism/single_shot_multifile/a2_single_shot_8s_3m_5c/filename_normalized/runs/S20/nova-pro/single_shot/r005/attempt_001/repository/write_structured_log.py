import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def write_structured_log(log_data):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = 'CustomLogs | extend timestamp = now(), log_data = dynamic({})'.format(log_data)
    response = client.query_workspace(os.getenv('LOG_ANALYTICS_WORKSPACE_ID'), query)
    if response.status == LogsQueryStatus.SUCCESS:
        print('Log written successfully')
    else:
        print('Log write failed')

# Example usage:
# write_structured_log({'event': 'user_login', 'user_id': '12345'})