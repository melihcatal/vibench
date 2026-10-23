from __future__ import annotations

from typing import Any, Dict, Optional

from google.cloud import monitoring_v3

from observability_client import build_filter, get_project_id, monitoring_client, time_interval_from_minutes
from observability_models import normalize_time_series


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    minutes: int = 15,
    resource_type: Optional[str] = None,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    client = monitoring_client()
    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{get_project_id(project_id)}",
        filter=build_filter(metric_type, resource_type, resource_labels, metric_labels),
        interval=monitoring_v3.TimeInterval(time_interval_from_minutes(minutes)),
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    series = list(client.list_time_series(request=request))
    normalized = normalize_time_series(metric_type, [monitoring_v3.TimeSeries.to_dict(item) for item in series])
    return {
        "metric_type": normalized.metric_type,
        "matched_points": [point.__dict__ for point in normalized.points],
        "unit": normalized.unit,
    }
