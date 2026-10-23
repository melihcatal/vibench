from __future__ import annotations

from typing import List, Optional

from observability_client import ObservabilityClient, create_client
from observability_models import (
    AggregationFunction,
    MetricAggregationResult,
    MetricQueryRequest,
    MetricTimeSeries,
    normalize_datadog_series,
)


def aggregate_metric_stats(
    metric_name: str,
    start: int,
    end: int,
    aggregation: AggregationFunction = AggregationFunction.AVG,
    tags: Optional[List[str]] = None,
    interval: Optional[int] = None,
    client: Optional[ObservabilityClient] = None,
) -> List[MetricAggregationResult]:
    query_prefix = aggregation.value
    tag_filter = ""
    if tags:
        tag_filter = "{" + ",".join(tags) + "}"
    query_str = f"{query_prefix}:{metric_name}{tag_filter}"

    if client is None:
        client = create_client()

    params = {
        "from": start,
        "to": end,
        "query": query_str,
    }
    if interval is not None:
        params["interval"] = interval

    response = client.query_metrics_v1(
        query=query_str,
        start=start,
        end=end,
        interval=interval,
    )

    results = []
    for raw_series in response.get("series", []):
        series = normalize_datadog_series(raw_series, metric_name)
        tag_set = series.tag_set

        point_count = len(series.points)
        agg_value = _compute_aggregation(series.points, aggregation)

        results.append(
            MetricAggregationResult(
                metric_name=metric_name,
                query=query_str,
                start=start,
                end=end,
                aggregation=aggregation,
                value=agg_value,
                point_count=point_count,
                tag_set=tag_set,
            )
        )

    return results


def _compute_aggregation(points: list, aggregation: AggregationFunction) -> float:
    if not points:
        return 0.0

    values = [p.value for p in points]

    if aggregation == AggregationFunction.AVG:
        return sum(values) / len(values)
    elif aggregation == AggregationFunction.SUM:
        return sum(values)
    elif aggregation == AggregationFunction.MIN:
        return min(values)
    elif aggregation == AggregationFunction.MAX:
        return max(values)
    elif aggregation == AggregationFunction.COUNT:
        return float(len(values))
    elif aggregation == AggregationFunction.RATE:
        if len(values) < 2:
            return 0.0
        sorted_points = sorted(points, key=lambda p: p.timestamp)
        time_diff = sorted_points[-1].timestamp - sorted_points[0].timestamp
        if time_diff == 0:
            return 0.0
        value_diff = sorted_points[-1].value - sorted_points[0].value
        return value_diff / time_diff
    else:
        return sum(values) / len(values)
