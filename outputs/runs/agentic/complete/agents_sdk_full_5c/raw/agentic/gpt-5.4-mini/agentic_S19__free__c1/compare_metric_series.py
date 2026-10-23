from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client, project_name, parse_filters
from observability_models import MetricSeriesComparisonRequest, normalize_time_series


def compare_metric_series(metric_type: str, minutes: int, left_labels: Dict[str, str], right_labels: Dict[str, str]) -> Dict[str, Any]:
    config = load_config()
    client = metric_client()
    now = datetime.now(timezone.utc)
    interval = monitoring_v3.TimeInterval({"start_time": now - timedelta(minutes=minutes), "end_time": now})
    req = MetricSeriesComparisonRequest(metric_type=metric_type, minutes=minutes, left_labels=left_labels, right_labels=right_labels)

    def fetch(labels: Dict[str, str]) -> list[float]:
        resp = client.list_time_series(
            request={
                "name": project_name(config),
                "filter": " AND ".join([f'metric.type = "{req.metric_type}"', parse_filters(labels)]),
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )
        return normalize_time_series(resp).values

    left = fetch(req.left_labels)
    right = fetch(req.right_labels)
    return {
        "metric_type": req.metric_type,
        "left": {"count": len(left), "mean": sum(left) / len(left) if left else 0.0},
        "right": {"count": len(right), "mean": sum(right) / len(right) if right else 0.0},
        "difference_mean": ((sum(left) / len(left)) if left else 0.0) - ((sum(right) / len(right)) if right else 0.0),
    }
