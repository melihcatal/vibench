from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client
from observability_models import MetricDimensionFilterRequest


def filter_metric_dimensions(request: MetricDimensionFilterRequest) -> Dict[str, Any]:
    config = load_config()
    client = metric_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=request.minutes)
    interval = monitoring_v3.TimeInterval({"end_time": end_time, "start_time": start_time})

    labels_filter = " ".join([f'resource.labels."{k}" = "{v}"' for k, v in request.labels.items()])
    base_filter = request.filter_expression or f'metric.type = "{request.metric_type}"'
    full_filter = " AND ".join([part for part in [base_filter, labels_filter] if part])

    series = client.list_time_series(
        request={
            "name": f"projects/{config.project_id}",
            "filter": full_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    matches: List[Dict[str, Any]] = []
    for ts in series:
        matches.append({"resource": dict(ts.resource.labels), "metric": dict(ts.metric.labels), "points": len(ts.points)})

    return {"metric_type": request.metric_type, "matches": matches, "filter": full_filter}
