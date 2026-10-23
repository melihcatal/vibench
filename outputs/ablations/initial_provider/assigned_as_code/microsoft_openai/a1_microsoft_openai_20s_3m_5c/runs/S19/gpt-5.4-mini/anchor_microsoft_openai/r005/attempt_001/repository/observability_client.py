import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def load_config(config=None):
    config = dict(config or {})
    if 'resource_id' not in config:
        config['resource_id'] = os.environ['AZURE_MONITOR_RESOURCE_ID']
    if 'period_seconds' not in config:
        config['period_seconds'] = int(os.environ.get('AZURE_MONITOR_PERIOD_SECONDS', '60'))
    if 'api_version' not in config:
        config['api_version'] = os.environ.get('AZURE_MONITOR_API_VERSION', '2023-10-01')
    return config


def create_metrics_client():
    credential = DefaultAzureCredential()
    return credential, MetricsQueryClient(credential)
