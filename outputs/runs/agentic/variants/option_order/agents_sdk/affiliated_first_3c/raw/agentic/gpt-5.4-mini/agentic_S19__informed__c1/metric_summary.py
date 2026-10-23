from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Any

from google.cloud import monitoring_v3

from observability_client import create_metric_client, project_name


def metric_summary(metric_type: str, window_hours: int = 24) -> Dict[str, Any]:
    client = create_metric_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=window_hours)
    interval = monitoring_v3.TimeInterval({"start_time": start_time, "end_time": end_time})
    metric_filter = f'metric.type = "{metric_type}"'
    values = []
    for series in client.list_time_series(name=project_name(), filter=metric_filter, interval=interval, view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL):
        for point in series.points:
            numeric = getattr(point.value, "double_value", None)
            if numeric is None:
                numeric = getattr(point.value, "int64_value", None)
            if numeric is not None:
                values.append(float(numeric))
    return {"metric_type": metric_type, "point_count": len(values), "min": min(values) if values else None, "max": max(values) if values else None, "average": (sum(values) / len(values)) if values else None, "source": "google-cloud-monitoring"}
