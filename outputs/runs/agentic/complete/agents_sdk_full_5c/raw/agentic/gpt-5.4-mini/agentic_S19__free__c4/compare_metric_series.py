from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict

from google.cloud import monitoring_v3

from observability_client import load_config, monitoring_client, project_name


def compare_metric_series(metric_type: str, left_labels: Dict[str, str], right_labels: Dict[str, str], minutes: int = 60) -> dict:
    config = load_config()
    client = monitoring_client()
    now = datetime.now(timezone.utc)
    interval = monitoring_v3.TimeInterval({"end_time": now, "start_time": now - timedelta(minutes=minutes)})

    def fetch(labels: Dict[str, str]) -> float:
        label_filters = " AND ".join([f'resource.label.{k} = "{v}"' for k, v in labels.items()])
        filt = f'metric.type = "{metric_type}"'
        if label_filters:
            filt = f"{filt} AND {label_filters}"
        series = client.list_time_series(
            request={"name": project_name(config.project_id), "filter": filt, "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL}
        )
        total = 0.0
        for item in series:
            for point in item.points:
                if hasattr(point.value, "double_value"):
                    total += float(point.value.double_value)
                elif hasattr(point.value, "int64_value"):
                    total += float(point.value.int64_value)
        return total

    return {"left_total": fetch(left_labels), "right_total": fetch(right_labels), "difference": fetch(left_labels) - fetch(right_labels)}
