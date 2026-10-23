import os

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

# [SAME-SCENARIO] compare_metric_series.py


def compare_metric_series(
    metric_name, resource_id_1, resource_id_2, start_time, end_time
):
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    metrics_1 = client.query(
        resource_uri=resource_id_1,
        metricnames=[metric_name],
        timespan=(start_time, end_time),
    )
    metrics_2 = client.query(
        resource_uri=resource_id_2,
        metricnames=[metric_name],
        timespan=(start_time, end_time),
    )
    return metrics_1, metrics_2
