from datetime import datetime, timezone

from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def get_config(config=None):
    return config or {}


def get_credential():
    return DefaultAzureCredential()


def get_client(credential=None):
    return MetricsQueryClient(credential or DefaultAzureCredential())


def to_datetime(value):
    return datetime.fromtimestamp(value, tz=timezone.utc)
