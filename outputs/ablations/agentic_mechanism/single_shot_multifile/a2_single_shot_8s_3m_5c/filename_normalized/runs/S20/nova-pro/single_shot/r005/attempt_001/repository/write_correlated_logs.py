import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

def write_correlated_logs(logs):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    for log in logs:
        query = 'CustomLogs | extend timestamp = now(), log_data = dynamic({})'.format(log)
        response = client.query_workspace(os.getenv('LOG_ANALYTICS_WORKSPACE_ID'), query)
        if response.status == LogsQueryStatus.SUCCESS:
            print('Log written successfully')
        else:
            print('Log write failed')

# Example usage:
# write_correlated_logs([{'event': 'user_login', 'user_id': '12345', 'correlation_id': 'abcde'}, {'event': 'user_logout', 'user_id': '12345', 'correlation_id': 'abcde'}])