from __future__ import annotations

from typing import Dict

from observability_models import MetricWindowRequest, summarize_change
from query_metric_window import query_metric_window


def compare_metric_series(
    metric: str,
    start_time,
    end_time,
    left_dimensions: Dict[str, str],
    right_dimensions: Dict[str, str],
    namespace: str = "AWS/EC2",
    period: int = 60,
    stat: str = "Average",
    region_name: str | None = None,
):
    left_request = MetricWindowRequest(
        metric=metric,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=left_dimensions,
    )
    right_request = MetricWindowRequest(
        metric=metric,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=right_dimensions,
    )
    left_series = query_metric_window(left_request, region_name=region_name)
    right_series = query_metric_window(right_request, region_name=region_name)
    return {
        "left": left_series,
        "right": right_series,
        "comparison": summarize_change(left_series, right_series),
    }
