import os
from azure.identity import DefaultAzureCredential


def get_config():
    return {
        'resource_id': os.getenv('AZURE_RESOURCE_ID'),
        'period_seconds': int(os.getenv('AZURE_PERIOD_SECONDS', 60))
    }


def get_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)