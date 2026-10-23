import os
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential

def get_logs_query_client():
    credential = DefaultAzureCredential()
    return LogsQueryClient(credential)

def get_workspace_id():
    return os.getenv('LOG_ANALYTICS_WORKSPACE_ID')