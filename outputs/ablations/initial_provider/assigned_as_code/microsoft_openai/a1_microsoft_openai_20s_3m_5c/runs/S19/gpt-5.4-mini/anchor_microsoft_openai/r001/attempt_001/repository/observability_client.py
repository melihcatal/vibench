import os
from datetime import timedelta

from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def load_observability_config(config=None):
    config = dict(config or {})
    if 'resource_id' not in config and os.getenv('AZURE_MONITOR_RESOURCE_ID'):
        config['resource_id'] = os.environ['AZURE_MONITOR_RESOURCE_ID']
    if 'period_seconds' not in config:
        config['period_seconds'] = int(os.getenv('AZURE_MONITOR_PERIOD_SECONDS', '60'))
    return config


def metric_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)


def period_to_timedelta(config):
    return timedelta(seconds=int(config.get('period_seconds', 60)))
