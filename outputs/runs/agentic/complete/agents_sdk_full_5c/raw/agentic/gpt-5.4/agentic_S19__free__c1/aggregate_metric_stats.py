from __future__ import annotations

from typing import Literal

from google.cloud import monitoring_v3

from observability_client import compute_interval, monitoring_client, project_name
from observability_models import AggregateStatsResponse, MetricWindowRequest, average, build_filter, parse_numeric_typed_value


GOOGLE_CLOUD_PROVIDER = "monitoring.googleapis.com"


_ALIGNERS = {
    "mean": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    "max": monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
    "min": monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
    "sum": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
}


from datetime import datetime


def aggregate_metric_stats(request: MetricWindowRequest, aggregation: Literal["mean", "max", "min", "sum"] = "mean") -> AggregateStatsResponse:
    client = monitoring_client()
    interval_start, interval_end = compute_interval(request.minutes)
    query_filter = build_filter(request.metric_type, request.resource_type, request.resource_labels, request.metric_labels)
    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(datetime.fromisoformat(interval_end.replace("Z", "+00:00")).timestamp())},
        start_time={"seconds": int(datetime.fromisoformat(interval_start.replace("Z", "+00:00")).timestamp())},
    )
    series_iter = client.list_time_series(
        request={
            "name": project_name(request.project_id),
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": monitoring_v3.Aggregation(
                alignment_period={"seconds": request.alignment_period_seconds},
                per_series_aligner=_ALIGNERS[assembly := aggregation],
            ),
        }
    )

    values = [parse_numeric_typed_value(point.value) for series in series_iter for point in series.points]
    if aggregation == "max":
        value = max(values) if values else 0.0
    elif aggregation == "min":
        value = min(values) if values else 0.0
    elif aggregation == "sum":
        value = sum(values)
    else:
        value = average(values)

    return AggregateStatsResponse(
        metric_type=request.metric_type,
        interval_start=interval_start,
        interval_end=interval_end,
        aggregation=assembly,
        value=value,
        sample_count=len(values),
    )
