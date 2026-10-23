from __future__ import annotations

import os
from datetime import timedelta
from typing import Any, Dict, Optional

from google.cloud import monitoring_v3

from observability_models import MetricWindowRequest, to_rfc3339


def get_google_cloud_project_id(explicit_project_id: Optional[str] = None) -> str:
    project_id = (
        explicit_project_id
        or os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("GCP_PROJECT")
    )
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT must be set")
    return project_id


def build_monitoring_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def build_project_name(project_id: Optional[str] = None) -> str:
    return f"projects/{get_google_cloud_project_id(project_id)}"


def build_time_interval(request: MetricWindowRequest) -> monitoring_v3.TimeInterval:
    return monitoring_v3.TimeInterval(
        {
            "start_time": {"seconds": int(_to_timestamp_seconds(request.start_time))},
            "end_time": {"seconds": int(_to_timestamp_seconds(request.end_time))},
        }
    )


def build_aggregation(request: MetricWindowRequest) -> monitoring_v3.Aggregation:
    return monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": request.alignment_period_seconds},
            "per_series_aligner": getattr(
                monitoring_v3.Aggregation.Aligner, request.aligner
            ),
        }
    )


def build_list_request(
    request: MetricWindowRequest, view: str = "FULL"
) -> Dict[str, Any]:
    return {
        "name": build_project_name(request.project_id),
        "filter": request.to_filter(),
        "interval": build_time_interval(request),
        "aggregation": build_aggregation(request),
        "view": getattr(monitoring_v3.ListTimeSeriesRequest.TimeSeriesView, view),
    }


def default_recent_window(
    metric_type: str, minutes: int = 30, project_id: Optional[str] = None
) -> MetricWindowRequest:
    from datetime import datetime, timezone

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    return MetricWindowRequest(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        project_id=project_id,
    )


def _to_timestamp_seconds(value: Any) -> float:
    if hasattr(value, "timestamp"):
        return float(value.timestamp())
    if isinstance(value, str):
        from datetime import datetime

        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).timestamp()
    raise TypeError(f"Unsupported time value: {value!r}")


def serialize_window_request(request: MetricWindowRequest) -> Dict[str, Any]:
    return {
        "metric_type": request.metric_type,
        "start_time": to_rfc3339(request.start_time),
        "end_time": to_rfc3339(request.end_time),
        "project_id": request.project_id,
        "resource_type": request.resource_type,
        "labels": dict(request.labels),
        "aligner": request.aligner,
        "alignment_period_seconds": request.alignment_period_seconds,
    }
