from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

def get_logs_query_client():
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    return client