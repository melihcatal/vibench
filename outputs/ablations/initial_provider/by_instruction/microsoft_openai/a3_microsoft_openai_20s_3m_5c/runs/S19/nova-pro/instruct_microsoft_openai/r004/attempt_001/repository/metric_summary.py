import os
from azure.monitor.query import MetricsQueryClient, MetricAggregationType
from azure.identity import DefaultAzureCredential
from observability_client import get_metrics_client, get_resource_uri
from observability_models import MetricDataPoint, MetricSeries

def metric_summary(metric_name, start_time, end_time):
    client = get_metrics_client()
    query = client.query_metric(
        metric_names=[metric_name],
        resource_uri=get_resource_uri(),
        timespan=(start_time, end_time),
        aggregations=[MetricAggregationType.AVERAGE]
    )
    data_points = [MetricDataPoint(point.timestamp, point.average) for point in query.metrics[0].time_series[0].data]
    series = MetricSeries(metric_name, data_points)
    return series