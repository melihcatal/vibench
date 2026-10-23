from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

class ObservabilityClient:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.client = LogsQueryClient(self.credential)

    def query_logs(self, query: str):
        response = self.client.query_workspace(workspace_id="your_workspace_id", query=query)
        if response.status == LogsQueryStatus.SUCCESS:
            return response.tables
        else:
            raise Exception(f"Query failed with status: {response.status}")

# Example usage:
# client = ObservabilityClient()
# results = client.query_logs("Heartbeat | take 10")
# print(results)