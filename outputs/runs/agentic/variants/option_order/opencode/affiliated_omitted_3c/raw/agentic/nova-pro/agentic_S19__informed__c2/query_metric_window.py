import os

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")

from azure.monitor.query import MetricsQueryClient

client = MetricsQueryClient(AZURE_CLIENT_ID)
