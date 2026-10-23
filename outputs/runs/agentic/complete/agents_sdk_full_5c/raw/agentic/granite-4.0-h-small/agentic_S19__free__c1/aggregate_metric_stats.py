import os
from observability_client import MetricsClient
from observability_models import MetricStatsRequest, MetricStatsResponse

def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str) -> None:
    """Retrieve aggregated statistics for a metric over a time window using the
    Datadog API.
    """
    client = MetricsClient()
    request = MetricStatsRequest(
        metric=metric_name,
        start=start_time,
        end=end_time,
        aggregation='sum',  # or 'avg', 'min', 'max', etc.
    )
    raw = client.aggregate_metric_stats(request)
    resp = MetricStatsResponse.from_dict(raw)
    print(resp.statistics)
