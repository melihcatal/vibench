import os
import time
from typing import Optional

from observability_models import (
    MetricQuery,
    MetricWindowResponse,
    AggregationFunction,
)
from observability_client import query_datadog_metrics


def query_metric_window(
    metric_name: str,
    start_ts: Optional[int] = None,
    end_ts: Optional[int] = None,
    aggregation: AggregationFunction = AggregationFunction.AVG,
    interval: int = 60,
    dimensions: Optional[dict[str, str]] = None,
) -> MetricWindowResponse:
    if end_ts is None:
        end_ts = int(time.time())
    if start_ts is None:
        start_ts = end_ts - 3600
    query = MetricQuery(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        aggregation=aggregation,
        interval=interval,
        dimensions=dimensions or {},
    )
    response = query_datadog_metrics(query)
    return response


if __name__ == "__main__":
    result = query_metric_window(
        metric_name=os.environ.get("DD_METRIC_NAME", "system.cpu.user"),
        start_ts=int(time.time()) - 3600,
        end_ts=int(time.time()),
        aggregation=AggregationFunction.AVG,
        interval=60,
    )
    print(f"Status: {result.status}")
    print(f"Series count: {len(result.series)}")
    for s in result.series:
        print(f"  {s.metric_name}: {len(s.datapoints)} datapoints")
