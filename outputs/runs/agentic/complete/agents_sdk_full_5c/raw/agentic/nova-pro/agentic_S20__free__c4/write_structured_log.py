import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential
from observability_models import StructuredLogModel

def write_structured_log(log_event: StructuredLogModel):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    query = log_event.to_query()
    response = client.query_workspace(os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID'), query)
    if response.status == LogsQueryStatus.SUCCESS:
        print('Log written successfully')
    else:
        print('Failed to write log')