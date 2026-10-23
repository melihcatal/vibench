from __future__ import annotations

from typing import List

from observability_models import MetricStatistics, MetricWindowRequest
from query_metric_window import query_metric_window


def aggregate_metric_stats(request: MetricWindowRequest) -> MetricStatistics:
    series_list = query_metric_window(request)
    values: List[float] = [
        point.value for series in series_list for point in series.points
    ]
    if not values:
        return MetricStatistics(
            metric_type=request.metric_type,
            start_time=request.start_rfc3339(),
            end_time=request.end_rfc3339(),
            count=0,
            minimum=None,
            maximum=None,
            average=None,
            sum=None,
        )
    total = float(sum(values))
    return MetricStatistics(
        metric_type=request.metric_type,
        start_time=request.start_rfc3339(),
        end_time=request.end_rfc3339(),
        count=len(values),
        minimum=min(values),
        maximum=max(values),
        average=total / len(values),
        sum=total,
    )
