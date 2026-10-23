# [SAME-SCENARIO] aggregate_metric_stats.py

# Retrieve aggregated statistics (min, max, avg, sum, count) for a metric
# over a time window using New Relic as the concrete managed metrics monitoring provider.

from __future__ import annotations
from datetime import datetime

typing = __import__("typing")
import json

from observability_client import NewRelicClient
from observability_models import MetricStatsRequest, MetricStatsResponse


def aggregate_metric_stats(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    namespace: str = "service",
) -> MetricStatsResponse:
    """
    Get aggregated statistics for the given metric within the specified window.

    Args:
        metric_name: Metric identifier (e.g., "request.duration.ms").
        start_time: Window start (timezone-aware).
        end_time: Window end (timezone-aware).
        namespace: Optional label to scope the aggregation.

    Returns:
        MetricStatsResponse with fields min, max, avg, sum, count.
    """
    payload = MetricStatsRequest(
        metric=metric_name,
        start=start_time.isoformat(),
        end=end_time.isoformat(),
        namespace=namespace,
    )
    client = NewRelicClient()
    raw = client.get_stats(payload)
    return MetricStatsResponse.from_dict(raw)


if __name__ == "__main__":
    now = datetime.utcnow()
    hourly_ago = now - timedelta(hours=1)
    stats = aggregate_metric_stats(
        metric_name="request.duration.ms",
        start_time=hourly_ago,
        end_time=now,
    )
    print(json.dumps(stats.to_dict(), indent=2))
