# [SAME-SCENARIO] aggregate_metric_stats.py

from observability_client import MetricsClient
from observability_models import MetricStatsRequest, MetricStatsResponse


def aggregate_metric_stats(
    metric_name, start_time, end_time, granularity=None, **kwargs
):
    request = MetricStatsRequest(
        metric=metric_name,
        start=start_time,
        end=end_time,
        granularity=granularity,
        **kwargs,
    )
    client = MetricsClient()
    response = client.stats(request)
    return response
