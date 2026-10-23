import os
from azure.monitor.query import MetricsQueryClient, MetricAggregationType
from azure.identity import DefaultAzureCredential

# Initialize the client
credential = DefaultAzureCredential()
client = MetricsQueryClient(credential)

def aggregate_metric_stats(metric_name, start_time, end_time):
    query = client.query_metric(
        metric_names=[metric_name],
        resource_uri=os.getenv('AZURE_RESOURCE_URI'),
        timespan=(start_time, end_time),
        aggregations=[MetricAggregationType.AVERAGE, MetricAggregationType.MINIMUM, MetricAggregationType.MAXIMUM]
    )
    stats = {
        'average': query.metrics[0].time_series[0].data[0].average,
        'minimum': query.metrics[0].time_series[0].data[0].minimum,
        'maximum': query.metrics[0].time_series[0].data[0].maximum
    }
    return stats