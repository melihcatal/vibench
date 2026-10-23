import os
import time
from typing import Optional

from observability_models import (
    MetricQuery,
    MetricWindowResponse,
    AggregationFunction,
    DimensionFilter,
)
from observability_client import query_datadog_metrics


def filter_metric_dimensions(
    metric_name: str,
    dimension_filters: list[DimensionFilter],
    start_ts: Optional[int] = None,
    end_ts: Optional[int] = None,
    aggregation: AggregationFunction = AggregationFunction.AVG,
    interval: int = 60,
) -> MetricWindowResponse:
    if end_ts is None:
        end_ts = int(time.time())
    if start_ts is None:
        start_ts = end_ts - 3600
    dimensions = {}
    for f in dimension_filters:
        if f.operator == "eq":
            dimensions[f.dimension_key] = f.dimension_value
        elif f.operator == "neq":
            dimensions[f"not_{f.dimension_key}"] = f.dimension_value
        else:
            dimensions[f.dimension_key] = f.dimension_value
    query = MetricQuery(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        aggregation=aggregation,
        interval=interval,
        dimensions=dimensions,
    )
    response = query_datadog_metrics(query)
    return response


if __name__ == "__main__":
    filters = [
        DimensionFilter(dimension_key="host", dimension_value="web-01", operator="eq"),
        DimensionFilter(
            dimension_key="env", dimension_value="production", operator="eq"
        ),
    ]
    result = filter_metric_dimensions(
        metric_name=os.environ.get("DD_METRIC_NAME", "system.cpu.user"),
        dimension_filters=filters,
        start_ts=int(time.time()) - 3600,
        end_ts=int(time.time()),
        aggregation=AggregationFunction.AVG,
        interval=60,
    )
    print(f"Status: {result.status}")
    print(f"Series count: {len(result.series)}")
