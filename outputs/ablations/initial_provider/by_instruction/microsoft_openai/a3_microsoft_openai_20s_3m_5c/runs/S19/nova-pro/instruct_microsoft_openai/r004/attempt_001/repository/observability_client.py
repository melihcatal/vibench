import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient

def get_metrics_client():
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    return client

def get_resource_uri():
    return os.getenv('AZURE_RESOURCE_URI')