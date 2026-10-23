import os
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential

def get_logs_query_client():
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    return client