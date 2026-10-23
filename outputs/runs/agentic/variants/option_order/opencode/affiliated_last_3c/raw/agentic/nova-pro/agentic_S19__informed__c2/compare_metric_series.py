import os

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

# [SAME-SCENARIO] compare_metric_series.py


def compare_metric_series(
    metric_name, start_time, end_time, dimension_filter1, dimension_filter2
):
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    result1 = client.query(
        resource_uri=os.getenv("AZURE_MONITOR_RESOURCE_URI"),
        metric_names=[metric_name],
        timespan=(start_time, end_time),
        filter=dimension_filter1,
    )
    result2 = client.query(
        resource_uri=os.getenv("AZURE_MONITOR_RESOURCE_URI"),
        metric_names=[metric_name],
        timespan=(start_time, end_time),
        filter=dimension_filter2,
    )
    return result1, result2
