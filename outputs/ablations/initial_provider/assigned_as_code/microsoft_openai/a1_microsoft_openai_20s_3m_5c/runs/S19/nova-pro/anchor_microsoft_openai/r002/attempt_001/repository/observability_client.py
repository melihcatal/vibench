from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def get_observability_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)


def normalize_metric_response(response):
    points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
               for metric in response.metrics for series in metric.timeseries
               for point in series.data if point.average is not None]
    return sorted(points, key=lambda point: point['timestamp'])