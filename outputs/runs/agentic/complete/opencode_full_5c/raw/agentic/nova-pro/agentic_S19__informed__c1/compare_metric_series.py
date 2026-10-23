import os
from azure.monitor.query import MetricsQueryClient
from azure.core.credentials import AzureKeyCredential


def compare_metric_series(metric_name, resource_1, resource_2, start_time, end_time):
    credential = AzureKeyCredential(os.getenv("AZURE_CLIENT_ID"))
    client = MetricsQueryClient(credential)
    # Compare implementation here
    pass
