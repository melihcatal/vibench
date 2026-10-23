# [SAME-SCENARIO] filter_metric_dimensions.py

# Query metric data filtered by resource labels or dimensions using New Relic as the provider.

from __future__ import annotations
from datetime import datetime

typing = __import__("typing")
import json

from observability_client import NewRelicClient
from observability_models import FilteredMetricRequest, FilteredMetricResponse


def filter_metric_dimensions(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimension_filters: typing.Dict[str, typing.List[str]],
) -> FilteredMetricResponse:
    """
    Retrieve datapoints for a metric that match the supplied dimension filters.

    Args:
        metric_name: Name of the metric (e.g., "http.request.count").
        start_time: Inclusive start of the time window (timezone-aware).
        end_time: Exclusive end of the time window (timezone-aware).
        dimension_filters: Dict where keys are dimension names and values are lists of allowed values.
            Example: {"host": ["web-01", "web-02"], "region": ["us-east"]}

    Returns:
        FilteredMetricResponse containing the filtered datapoints and matched dimensions metadata.
    """
    payload = FilteredMetricRequest(
        metric=metric_name,
        start=start_time.isoformat(),
        end=end_time.isoformat(),
        dimensions=dimension_filters,
    )
    client = NewRelicClient()
    raw = client.query_filtered_metrics(payload)
    return FilteredMetricResponse.from_dict(raw)


if __name__ == "__main__":
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    result = filter_metric_dimensions(
        metric_name="disk.usage.percent",
        start_time=one_hour_ago,
        end_time=now,
        dimension_filters={"host": ["app-server-01", "app-server-02"]},
    )
    print(json.dumps(result.to_dict(), indent=2))
