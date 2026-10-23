from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Mapping

from google.cloud import monitoring_v3

from observability_client import get_project_name, get_time_interval, monitoring_client
from observability_models import compare_series


def compare_metric_series(metric_name: str, left_filter: Mapping[str, str], right_filter: Mapping[str, str], minutes: int = 60) -> Dict[str, Any]:
    client = monitoring_client()
    project_name = get_project_name()
    now = datetime.now(timezone.utc)
    interval = get_time_interval(now - timedelta(minutes=minutes), now)

    def build_filter(extra: Mapping[str, str]) -> str:
        parts = [f'metric.type = "{metric_name}"']
        for key, value in extra.items():
            parts.append(f'{key} = "{value}"')
        return " AND ".join(parts)

    left_request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=build_filter(left_filter),
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    right_request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=build_filter(right_filter),
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    left_series = list(client.list_time_series(request=left_request))
    right_series = list(client.list_time_series(request=right_request))
    return compare_series(metric_name, interval.start_time, interval.end_time, left_series, right_series, dict(left_filter), dict(right_filter))
