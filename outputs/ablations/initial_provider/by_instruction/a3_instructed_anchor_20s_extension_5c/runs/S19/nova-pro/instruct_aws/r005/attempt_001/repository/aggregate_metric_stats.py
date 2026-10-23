import observability_client
from observability_models import MetricStatistics

def aggregate_metric_stats(metric_name, namespace, start_time, end_time, period=300):
    client = observability_client.get_cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Sum', 'Average', 'SampleCount', 'Minimum', 'Maximum'],
        Unit='Seconds'
    )
    return response