from __future__ import annotations

from typing import List

from google.cloud import monitoring_v3

from observability_client import compute_interval, monitoring_client, project_name
from observability_models import MetricSeriesPoint, MetricSeriesResponse, MetricWindowRequest, build_filter, parse_numeric_typed_value


GOOGLE_CLOUD_PROVIDER = "google-cloud-monitoring"


def query_metric_window(request: MetricWindowRequest) -> MetricSeriesResponse:
    client = monitoring_client()
    interval_start, interval_end = compute_interval(request.minutes)
    query_filter = build_filter(
        metric_type=request.metric_type,
        resource_type=request.resource_type,
        resource_labels=request.resource_labels,
        metric_labels=request.metric_labels,
    )
    interval = monitoring_v3.TimeInterval(end_time={"seconds": int(__import__("datetime").datetime.fromisoformat(interval_end.replace("Z", "+00:00")).timestamp())}, start_time={"seconds": int(__import__("datetime").datetime.fromisoformat(interval_start.replace("Z", "+00:00")).timestamp())})
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": request.alignment_period_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )

    series_iter = client.list_time_series(
        request={
            "name": project_name(request.project_id),
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    points: List[MetricSeriesPoint] = []
    for series in series_iter:
        for point in series.points:
            points.append(
                MetricSeriesPoint(
                    timestamp=point.interval.end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    value=parse_numeric_typed_value(point.value),
                    unit=getattr(series, "unit", None),
                    metric_labels=dict(series.metric.labels),
                    resource_labels=dict(series.resource.labels),
                )
            )

    points.sort(key=lambda item: item.timestamp)
    return MetricSeriesResponse(
        metric_type=request.metric_type,
        interval_start=interval_start,
        interval_end=interval_end,
        points=points,
    )
