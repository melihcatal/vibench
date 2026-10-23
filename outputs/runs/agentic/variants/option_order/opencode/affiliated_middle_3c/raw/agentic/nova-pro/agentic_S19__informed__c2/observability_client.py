# [HELPER] observability_client.py
import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def get_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)


def get_resource_id():
    return os.getenv("AZURE_RESOURCE_ID")
