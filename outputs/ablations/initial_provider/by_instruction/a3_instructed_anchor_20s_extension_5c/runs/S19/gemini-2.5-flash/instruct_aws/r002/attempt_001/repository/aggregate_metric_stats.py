import os
from datetime import datetime
from typing import Dict, Any, List
from observability_client import get_cloudwatch_client
from observability_models import MetricQuery

def aggregate_metric_stats(
    metric_query: MetricQuery,
    start_time: datetime,
    end_time: datetime,
    period: int = 300, # 5 minutes
    statistics: List[str] = None,
) -> Dict[str, Any]:
    """
    Retrieves aggregated statistics for a metric over a time window using AWS CloudWatch.
    """
    if statistics is None:
        statistics = ["Average", "Sum", "SampleCount", "Maximum", "Minimum"]

    cloudwatch = get_cloudwatch_client()

    response = cloudwatch.get_metric_statistics(
        Namespace=metric_query.namespace,
        MetricName=metric_query.metric_name,
        Dimensions=metric_query.to_cloudwatch_metric().get('Dimensions'),
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics,
    )

    return response.get('Datapoints', [])
