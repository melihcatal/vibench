from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


class ObservabilityClient:
    def __init__(self, resource_id: str):
        self.resource_id = resource_id
        self.credential = DefaultAzureCredential()
        self.metrics_client = MetricsQueryClient(self.credential)

    def get_metrics_client(self):
        return self.metrics_client

    def get_resource_id(self):
        return self.resource_id
