import os
from azure.identity import DefaultAzureCredential

def get_client():
    credential = DefaultAzureCredential()
    return LogsQueryClient(credential)

def get_workspace_id():
    return os.environ['AZURE_LOG_ANALYTICS_WORKSPACE_ID']"