from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient

def get_metrics_query_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)

def get_resource_id(config):
    return config.get('resource_id')
