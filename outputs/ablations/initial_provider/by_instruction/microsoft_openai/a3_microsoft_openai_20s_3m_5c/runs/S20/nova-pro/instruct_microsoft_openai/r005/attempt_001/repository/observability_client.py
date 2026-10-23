import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

def get_client():
    credential = DefaultAzureCredential()
    return LogsQueryClient(credential)

def get_workspace_id():
    return '<YOUR_WORKSPACE_ID>'