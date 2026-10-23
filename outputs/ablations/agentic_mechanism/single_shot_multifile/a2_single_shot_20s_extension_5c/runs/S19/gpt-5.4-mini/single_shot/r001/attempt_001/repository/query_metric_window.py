from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from google.cloud import monitoring_v3

from observability_client import get_project_name, get_time_interval, monitoring_client
from observability_models import MetricWindowQuery, normalize_points


def query_metric_window(metric_name: str, minutes: int = 60, resource_type: Optional[str] = None) -> Dict[str, Any]:
    client = monitoring_client()
    project_name = get_project_name()
    now = datetime.now(timezone.utc)
    interval = get_time_interval(now - timedelta(minutes=minutes), now)
    filter_parts = [f'metric.type = "{metric_name}"']
    if resource_type:
        filter_parts.append(f'resource.type = "{resource_type}"')
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=" AND ".join(filter_parts),
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    series = list(client.list_time_series(request=request))
    normalized = normalize_points(series)
    model = MetricWindowQuery(
        metric_name=metric_name,
        start_time=interval.start_time,
        end_time=interval.end_time,
        resource_type=resource_type,
        points=normalized,
    )
    return model.to_dict()
