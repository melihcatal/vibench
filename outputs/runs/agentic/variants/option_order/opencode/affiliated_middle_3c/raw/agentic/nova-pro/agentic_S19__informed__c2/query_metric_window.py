import os

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

# [SAME-SCENARIO] query_metric_window.py


def query_metric_window(metric_name, start_time, end_time):
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    metrics = client.query(
        resource_uri=os.environ["AZURE_RESOURCE_ID"],
        metricnames=[metric_name],
        timespan=(start_time, end_time),
        interval="PT1M",
    )
    return metrics
