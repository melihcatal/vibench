from __future__ import annotations

from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import load_config, monitoring_client, project_name
from observability_models import MetricAggregation


def aggregate_metric_stats(metric_type: str, minutes: int = 60) -> dict:
    config = load_config()
    client = monitoring_client()
    now = datetime.now(timezone.utc)
    interval = monitoring_v3.TimeInterval(
        {"end_time": now, "start_time": now - timedelta(minutes=minutes)}
    )
    series = client.list_time_series(
        request={
            "name": project_name(config.project_id),
            "filter": f'metric.type = "{metric_type}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    values = []
    for item in series:
        for point in item.points:
            if hasattr(point.value, "double_value"):
                values.append(float(point.value.double_value))
            elif hasattr(point.value, "int64_value"):
                values.append(float(point.value.int64_value))
    if not values:
        aggregation = MetricAggregation(metric_type, 0, 0.0, 0.0, 0.0, 0.0)
    else:
        aggregation = MetricAggregation(metric_type, len(values), min(values), max(values), sum(values) / len(values), sum(values))
    return aggregation.__dict__
