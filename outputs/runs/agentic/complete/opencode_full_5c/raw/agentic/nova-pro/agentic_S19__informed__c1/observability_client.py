import os
from azure.monitor.query import MetricsQueryClient
from azure.core.credentials import AzureKeyCredential


def get_client():
    credential = AzureKeyCredential(os.getenv("AZURE_CLIENT_ID"))
    client = MetricsQueryClient(credential)
    return client
