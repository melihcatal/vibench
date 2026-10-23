from __future__ import annotations

from typing import Any, Dict

from google.cloud import monitoring_v3

from observability_client import build_filter, get_project_id, monitoring_client, time_interval_from_minutes
from observability_models import MetricWindowRequest, normalize_time_series


def query_metric_window(
    project_id: str,
    metric_type: str,
    minutes: int = 15,
    alignment_period_seconds: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
) -> Dict[str, Any]:
    client = monitoring_client()
    name = f"projects/{get_project_id(project_id)}"
    interval = time_interval_from_minutes(minutes)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=name,
        filter=build_filter(metric_type=metric_type),
        interval=monitoring_v3.TimeInterval(interval),
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=monitoring_v3.Aggregation(
            alignment_period={"seconds": alignment_period_seconds},
            per_series_aligner=getattr(monitoring_v3.Aggregation.Aligner, per_series_aligner),
        ),
    )
    series = list(client.list_time_series(request=request))
    normalized = normalize_time_series(metric_type, [monitoring_v3.TimeSeries.to_dict(item) for item in series])
    return {
        "metric_type": normalized.metric_type,
        "unit": normalized.unit,
        "points": [point.__dict__ for point in normalized.points],
    }
