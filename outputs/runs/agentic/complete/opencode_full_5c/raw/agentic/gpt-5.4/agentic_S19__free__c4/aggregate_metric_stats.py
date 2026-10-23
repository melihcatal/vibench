from __future__ import annotations

from google.cloud.monitoring_v3.types import ListTimeSeriesRequest

from observability_client import (
    build_monitoring_filter,
    monitoring_client,
    project_resource_name,
)
from observability_models import (
    AggregatedStats,
    MetricWindowRequest,
    normalize_labels,
    parse_float,
)


ALIGNERS = {
    "mean": "ALIGN_MEAN",
    "max": "ALIGN_MAX",
    "min": "ALIGN_MIN",
    "sum": "ALIGN_SUM",
}


def aggregate_metric_stats(
    request: MetricWindowRequest, statistic: str = "mean"
) -> AggregatedStats:
    aligner = ALIGNERS.get(statistic.lower(), "ALIGN_MEAN")
    client = monitoring_client()
    series_iter = client.list_time_series(
        request={
            "name": project_resource_name(request.project_id),
            "filter": build_monitoring_filter(
                request.metric_type, request.filter_labels
            ),
            "interval": request.interval(),
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": {
                "alignment_period": {
                    "seconds": max(request.alignment_period_seconds, 60)
                },
                "per_series_aligner": aligner,
                "cross_series_reducer": "REDUCE_NONE",
            },
            "page_size": 1,
        }
    )
    series = next(iter(series_iter), None)
    point = series.points[0] if series and series.points else None
    value = parse_float(
        point.value._pb.ListFields()[0][1]
        if point and point.value._pb.ListFields()
        else None
    )
    labels = normalize_labels(dict(series.metric.labels)) if series else {}
    return AggregatedStats(
        metric_type=request.metric_type,
        statistic=statistic,
        start_time=request.interval()["start_time"],
        end_time=request.interval()["end_time"],
        value=value,
        labels=labels,
    )
