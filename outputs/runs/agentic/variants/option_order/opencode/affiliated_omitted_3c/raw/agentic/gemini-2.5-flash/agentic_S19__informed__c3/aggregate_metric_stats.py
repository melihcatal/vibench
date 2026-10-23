from datetime import datetime
import os

from observability_client import get_cloudwatch_client


def aggregate_metric_stats(
    metric_name: str,
    namespace: str,
    statistic: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,  # in seconds, default to 5 minutes
):
    client = get_cloudwatch_client()

    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic],
    )
    return response
