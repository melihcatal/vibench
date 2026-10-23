from __future__ import annotations

from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import load_config, monitoring_client, project_name


def metric_summary(metric_type: str, minutes: int = 30) -> dict:
    config = load_config()
    client = monitoring_client()
    now = datetime.now(timezone.utc)
    interval = monitoring_v3.TimeInterval({"end_time": now, "start_time": now - timedelta(minutes=minutes)})
    series = client.list_time_series(
        request={"name": project_name(config.project_id), "filter": f'metric.type = "{metric_type}"', "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL}
    )
    values = []
    for item in series:
        for point in item.points:
            if hasattr(point.value, "double_value"):
                values.append(float(point.value.double_value))
            elif hasattr(point.value, "int64_value"):
                values.append(float(point.value.int64_value))
    return {"metric_type": metric_type, "points": len(values), "latest": values[-1] if values else None, "average": (sum(values) / len(values)) if values else None}
