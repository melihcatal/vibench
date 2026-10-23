import datetime
from observability_client import get_cloudwatch_client

def aggregate_metric_stats(
    metric_name: str,
    namespace: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int = 300, # seconds
    statistics: list[str] = ['Average'],
    unit: str = 'None',
):
    client = get_cloudwatch_client()

    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics,
        Unit=unit,
    )
    return response

