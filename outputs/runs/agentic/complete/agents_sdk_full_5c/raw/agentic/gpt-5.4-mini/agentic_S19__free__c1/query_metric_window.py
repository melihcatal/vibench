from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client, project_name, parse_filters
from observability_models import MetricWindowRequest, normalize_time_series


def query_metric_window(metric_type: str, minutes: int, resource_labels: Dict[str, str] | None = None) -> Dict[str, Any]:
    config = load_config()
    client = metric_client()
    now = datetime.now(timezone.utc)
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": now - timedelta(minutes=minutes),
            "end_time": now,
        }
    )
    request = MetricWindowRequest(metric_type=metric_type, minutes=minutes, resource_labels=resource_labels or {})
    name = project_name(config)
    filter_parts = [f'metric.type = "{request.metric_type}"']
    if request.resource_labels:
        filter_parts.append(parse_filters(request.resource_labels))
    response = client.list_time_series(
        request={
            "name": name,
            "filter": " AND ".join(filter_parts),
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": {
                "alignment_period": {"seconds": request.alignment_period_seconds},
                "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            },
        }
    )
    normalized = normalize_time_series(response)
    return {
        "metric_type": normalized.metric_type,
        "values": normalized.values,
        "timestamps": [ts.isoformat() for ts in normalized.timestamps],
    }
