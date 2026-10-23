from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Mapping, Optional

from google.cloud import monitoring_v3

from observability_client import get_project_name, get_time_interval, monitoring_client
from observability_models import DimensionFilteredMetric, normalize_points_with_dimensions


def filter_metric_dimensions(metric_name: str, dimensions: Mapping[str, str], minutes: int = 60) -> Dict[str, Any]:
    client = monitoring_client()
    project_name = get_project_name()
    now = datetime.now(timezone.utc)
    interval = get_time_interval(now - timedelta(minutes=minutes), now)
    filters = [f'metric.type = "{metric_name}"']
    for key, value in dimensions.items():
        filters.append(f'metric.labels.{key} = "{value}"')
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=" AND ".join(filters),
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    series = list(client.list_time_series(request=request))
    normalized = normalize_points_with_dimensions(series)
    model = DimensionFilteredMetric(
        metric_name=metric_name,
        start_time=interval.start_time,
        end_time=interval.end_time,
        dimensions=dict(dimensions),
        series=normalized,
    )
    return model.to_dict()
