import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def load_config(config=None):
    config = dict(config or {})
    if 'resource_id' not in config and os.getenv('AZURE_MONITOR_RESOURCE_ID'):
        config['resource_id'] = os.environ['AZURE_MONITOR_RESOURCE_ID']
    return config


def get_metrics_client():
    return MetricsQueryClient(DefaultAzureCredential())
