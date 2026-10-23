import os

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

# [SAME-SCENARIO] aggregate_metric_stats.py


def aggregate_metric_stats(metric_name, start_time, end_time):
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    metrics = client.query(
        resource_uri=os.environ["AZURE_RESOURCE_ID"],
        metricnames=[metric_name],
        timespan=(start_time, end_time),
        aggregation=["Average", "Minimum", "Maximum", "Total"],
    )
    return metrics
