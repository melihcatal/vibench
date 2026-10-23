import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

# Azure Monitor Logs credentials
credential = DefaultAzureCredential()

# Create a client
client = LogsQueryClient(credential)

# Define the query
query = "customEvents | where timestamp > ago(1h)"

# Execute the query
response = client.query_workspace(os.environ["AZURE_LOG_ANALYTICS_WORKSPACE_ID"], query)

# Check the status of the query
if response.status == LogsQueryStatus.SUCCESS:
    for row in response.tables[0].rows:
        print(row)
else:
    print("Query failed: ", response.partial_error)
