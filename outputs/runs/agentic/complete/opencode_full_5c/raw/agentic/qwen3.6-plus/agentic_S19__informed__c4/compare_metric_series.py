import os
import time
from typing import Optional

from observability_models import (
    MetricComparison,
    MetricComparisonResponse,
    AggregationFunction,
)
from observability_client import compare_datadog_series


def compare_metric_series(
    metric_name: str,
    series_a_dimensions: dict[str, str],
    series_b_dimensions: dict[str, str],
    start_ts: Optional[int] = None,
    end_ts: Optional[int] = None,
    aggregation: AggregationFunction = AggregationFunction.AVG,
    interval: int = 60,
) -> MetricComparisonResponse:
    if end_ts is None:
        end_ts = int(time.time())
    if start_ts is None:
        start_ts = end_ts - 3600
    comparison = MetricComparison(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        series_a=series_a_dimensions,
        series_b=series_b_dimensions,
        aggregation=aggregation,
        interval=interval,
    )
    response = compare_datadog_series(comparison)
    return response


if __name__ == "__main__":
    result = compare_metric_series(
        metric_name=os.environ.get("DD_METRIC_NAME", "system.cpu.user"),
        series_a_dimensions={"host": "web-01", "env": "production"},
        series_b_dimensions={"host": "web-02", "env": "production"},
        start_ts=int(time.time()) - 3600,
        end_ts=int(time.time()),
        aggregation=AggregationFunction.AVG,
        interval=60,
    )
    print(f"Status: {result.status}")
    print(f"Delta avg: {result.delta_avg}")
    print(f"Delta pct: {result.delta_pct}%")
