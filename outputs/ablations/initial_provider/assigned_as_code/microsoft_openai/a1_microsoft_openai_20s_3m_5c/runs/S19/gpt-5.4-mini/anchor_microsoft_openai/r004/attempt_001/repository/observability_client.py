import os

from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def load_config(config=None):
    merged = dict(config or {})
    merged.setdefault('resource_id', os.environ.get('AZURE_MONITOR_RESOURCE_ID'))
    merged.setdefault('region', os.environ.get('AZURE_REGION'))
    merged.setdefault('period_seconds', int(os.environ.get('AZURE_METRIC_PERIOD_SECONDS', '60')))
    merged.setdefault('metric', os.environ.get('AZURE_MONITOR_METRIC_NAME'))
    return merged


def get_metrics_client():
    return MetricsQueryClient(DefaultAzureCredential())


def query_client(config=None):
    return get_metrics_client(), load_config(config)
