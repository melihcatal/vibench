import os
from azure.monitor.query import MetricsQueryClient, MetricAggregationType
from azure.identity import DefaultAzureCredential

# Initialize the client
credential = DefaultAzureCredential()
client = MetricsQueryClient(credential)

def filter_metric_dimensions(metric_name, start_time, end_time, dimension_name, dimension_value):
    query = client.query_metric(
        metric_names=[metric_name],
        resource_uri=os.getenv('AZURE_RESOURCE_URI'),
        timespan=(start_time, end_time),
        aggregations=[MetricAggregationType.AVERAGE],
        filter=f"{dimension_name} eq '{dimension_value}'"
    )
    data_points = [point for point in query.metrics[0].time_series[0].data]
    return data_points