from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

def get_client():
    credential = DefaultAzureCredential()
    return LogsQueryClient(credential)