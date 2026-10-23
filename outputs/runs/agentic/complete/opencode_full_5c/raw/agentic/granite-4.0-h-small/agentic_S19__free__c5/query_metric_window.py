# [SAME-SCENARIO] query_metric_window.py

# This file demonstrates querying recent datapoints for a named metric over a time window
# using New Relic as the concrete managed metrics monitoring provider.

from __future__ import annotations
from datetime import datetime, timedelta
import json

# Import the concrete provider client wrapper defined in the helper file.
from observability_client import NewRelicClient
from observability_models import MetricQueryRequest, MetricQueryResponse


def query_metric_window(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    namespace: str = "service",
    limit: int = 100,
) -> MetricQueryResponse:
    """Query raw datapoints for a metric within a specified time window.

    Args:
        metric_name: The metric identifier (e.g., "cpu.usage.percent").
        start_time: Inclusive start of the window (timezone-aware).
        end_time: Exclusive end of the window (timezone-aware).
        namespace: Optional resource label to scope the query.
        limit: Maximum number of data points to return.

    Returns:
        A MetricQueryResponse containing the raw datapoints and metadata.
    """
    # Translate Python datetime to ISO 8601 strings required by the provider API.
    payload = MetricQueryRequest(
        metric=metric_name,
        start=start_time.isoformat(),
        end=end_time.isoformat(),
        limit=limit,
        namespace=namespace,
    )
    # NewRelicClient is a thin wrapper around New Relic's Python SDK that handles auth.
    client = NewRelicClient()
    raw_response = client.query_metrics(payload)
    # Normalize the provider's raw response into our internal model.
    return MetricQueryResponse.from_dict(raw_response)


if __name__ == "__main__":
    # Example usage – fetch last 5 minutes of CPU usage data.
    now = datetime.utcnow()
    five_minutes_ago = now - timedelta(minutes=5)
    result = query_metric_window(
        metric_name="cpu.usage.percent",
        start_time=five_minutes_ago,
        end_time=now,
    )
    print(json.dumps(result.to_dict(), indent=2))
