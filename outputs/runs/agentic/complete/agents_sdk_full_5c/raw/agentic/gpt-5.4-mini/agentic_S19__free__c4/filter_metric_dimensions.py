from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, List

from google.cloud import monitoring_v3

from observability_client import load_config, monitoring_client, project_name
from observability_models import normalize_point


def filter_metric_dimensions(metric_type: str, labels: Dict[str, str], minutes: int = 60) -> List[dict]:
    config = load_config()
    client = monitoring_client()
    now = datetime.now(timezone.utc)
    interval = monitoring_v3.TimeInterval({"end_time": now, "start_time": now - timedelta(minutes=minutes)})
    label_filters = " AND ".join([f'resource.label.{k} = "{v}"' for k, v in labels.items()])
    base_filter = f'metric.type = "{metric_type}"'
    full_filter = f"{base_filter} AND {label_filters}" if label_filters else base_filter
    series = client.list_time_series(
        request={
            "name": project_name(config.project_id),
            "filter": full_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return [normalize_point(point).__dict__ for item in series for point in item.points]
