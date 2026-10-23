import os

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

# [SAME-SCENARIO] filter_metric_dimensions.py


def filter_metric_dimensions(metric_name, dimension_filter, start_time, end_time):
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    metrics = client.query(
        resource_uri=os.environ["AZURE_RESOURCE_ID"],
        metricnames=[metric_name],
        timespan=(start_time, end_time),
        filter=dimension_filter,
    )
    return metrics
