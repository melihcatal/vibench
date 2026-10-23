import os
from azure.monitor.query import MetricsQueryClient

def get_client():
    return MetricsQueryClient(os.getenv('AZURE_TENANT_ID'), os.getenv('AZURE_CLIENT_ID'))
