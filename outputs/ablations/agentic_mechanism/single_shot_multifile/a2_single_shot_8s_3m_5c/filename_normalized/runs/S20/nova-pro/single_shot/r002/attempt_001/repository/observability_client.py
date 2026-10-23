from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

def get_logs_query_client():
    credential = DefaultAzureCredential()
    return LogsQueryClient(credential)

def query_workspace(client, workspace_id, query):
    return client.query_workspace(workspace_id, query)