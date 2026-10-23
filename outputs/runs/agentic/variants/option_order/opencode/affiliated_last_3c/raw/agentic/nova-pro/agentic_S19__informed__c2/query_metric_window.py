import os

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

# [SAME-SCENARIO] query_metric_window.py


def query_metric_window(metric_name, start_time, end_time):
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    result = client.query(
        resource_uri=os.getenv("AZURE_MONITOR_RESOURCE_URI"),
        metric_names=[metric_name],
        timespan=(start_time, end_time),
    )
    return result
