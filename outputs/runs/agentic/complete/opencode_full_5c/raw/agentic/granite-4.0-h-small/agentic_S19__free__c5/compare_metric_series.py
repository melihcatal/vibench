# [SAME-SCENARIO] compare_metric_series.py

# Compare metric values for two different resources or dimension filters over the same time window.

from __future__ import annotations
from datetime import datetime

typing = __import__("typing")
import json

from observability_client import NewRelicClient
from observability_models import CompareRequest, CompareResponse


def compare_metric_series(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    left_filter: typing.Dict[str, typing.List[str]],
    right_filter: typing.Dict[str, typing.List[str]],
) -> CompareResponse:
    """
    Compare two series of the same metric using independent dimension filters.

    Args:
        metric_name: Metric identifier.
        start_time: Window start (timezone-aware).
        end_time: Window end (timezone-aware).
        left_filter: Dimension filter for the left series (e.g., a specific service).
        right_filter: Dimension filter for the right series (e.g., another service or environment).

    Returns:
        CompareResponse containing side-by-side values, delta, and percentage change.
    """
    payload = CompareRequest(
        metric=metric_name,
        start=start_time.isoformat(),
        end=end_time.isoformat(),
        left_filter=left_filter,
        right_filter=right_filter,
    )
    client = NewRelicClient()
    raw = client.compare_series(payload)
    return CompareResponse.from_dict(raw)


if __name__ == "__main__":
    now = datetime.utcnow()
    one_day_ago = now - timedelta(days=1)
    left = {"host": ["web-01"]}
    right = {"host": ["web-02"]}
    comparison = compare_metric_series(
        metric_name="request.rate",
        start_time=one_day_ago,
        end_time=now,
        left_filter=left,
        right_filter=right,
    )
    print(json.dumps(comparison.to_dict(), indent=2))
