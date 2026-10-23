import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential


def write_structured_log(log_event):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    response = client.query_workspace(
        os.environ["AZURE_LOG_ANALYTICS_WORKSPACE_ID"], log_event
    )
    if response.status == LogsQueryStatus.SUCCESS:
        print("Log written successfully")
    else:
        print("Failed to write log")
