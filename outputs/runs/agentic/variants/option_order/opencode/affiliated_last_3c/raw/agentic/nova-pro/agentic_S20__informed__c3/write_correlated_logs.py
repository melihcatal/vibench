import os
import uuid
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

# Azure Monitor Logs credentials
credential = DefaultAzureCredential()

# Create a client
client = LogsQueryClient(credential)

# Generate a correlation ID
correlation_id = str(uuid.uuid4())

# Define the log event
log_event = {
    "correlation_id": correlation_id,
    "message": "This is a correlated log event",
    "severity": "Informational",
}

# Convert the log event to a JSON string
log_event_json = json.dumps(log_event)

# Define the query
query = f'customEvents | where customDimensions.correlation_id == "{correlation_id}"'

# Execute the query
response = client.query_workspace(os.environ["AZURE_LOG_ANALYTICS_WORKSPACE_ID"], query)

# Check the status of the query
if response.status == LogsQueryStatus.SUCCESS:
    for row in response.tables[0].rows:
        print(row)
else:
    print("Query failed: ", response.partial_error)
