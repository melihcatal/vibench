from __future__ import annotations

from typing import Dict

from observability_models import ComparisonResponse, MetricSeriesResponse, MetricWindowRequest
from query_metric_window import query_metric_window



def compare_metric_series(
    left_dimensions: Dict[str, str],
    right_dimensions: Dict[str, str],
    *,
    metric_name: str,
    start_time,
    end_time,
    namespace: str = "AWS/EC2",
    period: int = 300,
    statistic: str = "Average",
    region_name: str | None = None,
) -> ComparisonResponse:
    left = query_metric_window(
        MetricWindowRequest(
            metric_name=metric_name,
            start_time=start_time,
            end_time=end_time,
            namespace=namespace,
            period=period,
            statistic=statistic,
            dimensions=left_dimensions,
            region_name=region_name,
        )
    )
    right = query_metric_window(
        MetricWindowRequest(
            metric_name=metric_name,
            start_time=start_time,
            end_time=end_time,
            namespace=namespace,
            period=period,
            statistic=statistic,
            dimensions=right_dimensions,
            region_name=region_name,
        )
    )
    right_index = {point.timestamp: point for point in right.datapoints}
    deltas = []
    for left_point in left.datapoints:
        right_point = right_index.get(left_point.timestamp)
        if right_point is None:
            continue
        deltas.append(
            {
                "timestamp": left_point.timestamp.isoformat(),
                "left_value": left_point.value,
                "right_value": right_point.value,
                "delta": left_point.value - right_point.value,
                "unit": left_point.unit or right_point.unit,
            }
        )
    return ComparisonResponse(left=left, right=right, delta_by_timestamp=deltas)
