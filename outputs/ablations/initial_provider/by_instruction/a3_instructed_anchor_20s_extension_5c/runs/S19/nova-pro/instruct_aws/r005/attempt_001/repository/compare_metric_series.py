import observability_client
from observability_models import MetricQuery

def compare_metric_series(metric_name, namespace, dimensions1, dimensions2, start_time, end_time, period=300):
    client = observability_client.get_cloudwatch_client()
    response1 = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions1,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average'],
        Unit='Seconds'
    )
    response2 = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions2,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average'],
        Unit='Seconds'
    )
    return response1, response2