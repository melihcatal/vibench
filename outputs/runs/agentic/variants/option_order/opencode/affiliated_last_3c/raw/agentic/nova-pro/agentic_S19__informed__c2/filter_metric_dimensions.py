import os

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

# [SAME-SCENARIO] filter_metric_dimensions.py


def filter_metric_dimensions(metric_name, start_time, end_time, dimension_filter):
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    result = client.query(
        resource_uri=os.getenv("AZURE_MONITOR_RESOURCE_URI"),
        metric_names=[metric_name],
        timespan=(start_time, end_time),
        filter=dimension_filter,
    )
    return result
