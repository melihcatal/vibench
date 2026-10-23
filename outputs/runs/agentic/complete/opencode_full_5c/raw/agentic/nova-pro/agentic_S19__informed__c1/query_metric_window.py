import os
from azure.monitor.query import MetricsQueryClient
from azure.core.credentials import AzureKeyCredential


def query_metric_window(metric_name, start_time, end_time):
    credential = AzureKeyCredential(os.getenv("AZURE_CLIENT_ID"))
    client = MetricsQueryClient(credential)
    # Query implementation here
    pass
