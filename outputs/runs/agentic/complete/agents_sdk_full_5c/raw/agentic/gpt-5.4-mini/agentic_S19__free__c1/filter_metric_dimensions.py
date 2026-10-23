from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client, project_name, parse_filters
from observability_models import normalize_time_series


def filter_metric_dimensions(metric_type: str, minutes: int, dimensions: Dict[str, str]) -> Dict[str, Any]:
    config = load_config()
    client = metric_client()
    now = datetime.now(timezone.utc)
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": now - timedelta(minutes=minutes),
            "end_time": now,
        }
    )
    filter_expr = " AND ".join([f'metric.type = "{metric_type}"', parse_filters(dimensions)])
    response = client.list_time_series(
        request={
            "name": project_name(config),
            "filter": filter_expr,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    normalized = normalize_time_series(response)
    return {"metric_type": normalized.metric_type, "values": normalized.values, "dimension_filter": dimensions}
