from azure.monitor.query import MetricsQueryClient, MetricAggregationType
from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential

def get_metrics_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)

def format_timespan(start_time, end_time):
    start = datetime.fromtimestamp(start_time, tz=timezone.utc)
    end = datetime.fromtimestamp(end_time, tz=timezone.utc)
    return (start, end)