import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

# Azure Monitor Logs credentials
credential = DefaultAzureCredential()

# Create a client
client = LogsQueryClient(credential)


# Define a function to execute a query
def execute_query(query):
    response = client.query_workspace(
        os.environ["AZURE_LOG_ANALYTICS_WORKSPACE_ID"], query
    )
    if response.status == LogsQueryStatus.SUCCESS:
        return response.tables[0].rows
    else:
        return f"Query failed: {response.partial_error}"


# Define a function to normalize log events
def normalize_log_event(log_event):
    return {
        "correlation_id": log_event.get("correlation_id", ""),
        "message": log_event.get("message", ""),
        "severity": log_event.get("severity", ""),
    }
