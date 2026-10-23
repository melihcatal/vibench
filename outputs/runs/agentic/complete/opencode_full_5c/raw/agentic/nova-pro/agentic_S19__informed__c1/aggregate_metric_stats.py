import os
from azure.monitor.query import MetricsQueryClient
from azure.core.credentials import AzureKeyCredential


def aggregate_metric_stats(metric_name, start_time, end_time):
    credential = AzureKeyCredential(os.getenv("AZURE_CLIENT_ID"))
    client = MetricsQueryClient(credential)
    # Aggregate implementation here
    pass
