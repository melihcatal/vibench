from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def get_observability_client():
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    return client