import os

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

# [SAME-SCENARIO] aggregate_metric_stats.py


def aggregate_metric_stats(metric_name, start_time, end_time):
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    result = client.query(
        resource_uri=os.getenv("AZURE_MONITOR_RESOURCE_URI"),
        metric_names=[metric_name],
        timespan=(start_time, end_time),
        aggregations=["Average", "Minimum", "Maximum", "Total"],
    )
    return result
