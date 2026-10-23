from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient

class AzureMonitorClient:
    def __init__(self):
        self.credential = DefaultAzureCredential()

    def get_metrics_query_client(self):
        return MetricsQueryClient(self.credential)
