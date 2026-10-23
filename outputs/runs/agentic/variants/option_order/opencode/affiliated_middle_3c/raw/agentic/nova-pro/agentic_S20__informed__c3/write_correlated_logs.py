import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential


def write_correlated_logs(log_events, correlation_id):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    for log_event in log_events:
        log_event["correlation_id"] = correlation_id
        response = client.query_workspace(
            os.environ["AZURE_LOG_ANALYTICS_WORKSPACE_ID"], log_event
        )
        if response.status == LogsQueryStatus.SUCCESS:
            print("Correlated log written successfully")
        else:
            print("Failed to write correlated log")
