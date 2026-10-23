from datetime import datetime
from typing import Any, Dict

from observability_client import ManagedMetricsClient
from observability_models import (
    MetricWindowRequest,
    normalize_dimensions,
    normalize_points,
)


def query_metric_window(
    project_id: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimensions: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    client = ManagedMetricsClient(project_id)
    request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions=normalize_dimensions(dimensions),
    )
    filter_parts = [f'metric.type="{request.metric_name}"']
    for key, value in request.dimensions.items():
        filter_parts.append(f'resource.labels."{key}"="{value}"')
    payload = client.query_time_series(
        request.metric_name,
        request.start_time,
        request.end_time,
        " AND ".join(filter_parts),
        view="FULL",
    )
    payload["timeSeries"] = [
        dict(series, points=normalize_points(series.get("points", [])))
        for series in payload.get("timeSeries", [])
    ]
    return payload
