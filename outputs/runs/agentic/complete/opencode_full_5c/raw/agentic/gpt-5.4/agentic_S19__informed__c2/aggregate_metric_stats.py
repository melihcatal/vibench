from __future__ import annotations

from statistics import mean

from observability_client import run_query
from observability_models import (
    AggregatedMetricStats,
    MetricWindowRequest,
    values_from_points,
)


def aggregate_metric_stats(request: MetricWindowRequest) -> AggregatedMetricStats:
    points = run_query(request)
    values = values_from_points(points)
    start_time = points[0].interval_start or points[0].interval_end if points else None
    end_time = points[-1].interval_end if points else None
    return AggregatedMetricStats(
        metric_type=request.metric_type,
        start_time=start_time or "",
        end_time=end_time or "",
        point_count=len(values),
        minimum=min(values) if values else None,
        maximum=max(values) if values else None,
        average=mean(values) if values else None,
        total=sum(values) if values else None,
    )
