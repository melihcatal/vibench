import os
from azure.monitor.query import MetricsQueryClient, MetricAggregationType
from azure.identity import DefaultAzureCredential

# Initialize the client
credential = DefaultAzureCredential()
client = MetricsQueryClient(credential)

def compare_metric_series(metric_name, start_time, end_time, dimension_name, dimension_value1, dimension_value2):
    query1 = client.query_metric(
        metric_names=[metric_name],
        resource_uri=os.getenv('AZURE_RESOURCE_URI'),
        timespan=(start_time, end_time),
        aggregations=[MetricAggregationType.AVERAGE],
        filter=f"{dimension_name} eq '{dimension_value1}'"
    )
    query2 = client.query_metric(
        metric_names=[metric_name],
        resource_uri=os.getenv('AZURE_RESOURCE_URI'),
        timespan=(start_time, end_time),
        aggregations=[MetricAggregationType.AVERAGE],
        filter=f"{dimension_name} eq '{dimension_value2}'"
    )
    series1 = [point.average for point in query1.metrics[0].time_series[0].data]
    series2 = [point.average for point in query2.metrics[0].time_series[0].data]
    return series1, series2