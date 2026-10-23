import observability_client
from observability_models import MetricQuery

def filter_metric_dimensions(metric_name, namespace, dimensions, start_time, end_time, period=300):
    client = observability_client.get_cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average'],
        Unit='Seconds'
    )
    return response