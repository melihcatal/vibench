from datetime import datetime
from typing import Any, Dict

from observability_client import ManagedMetricsClient
from observability_models import MetricWindowRequest, normalize_dimensions


def aggregate_metric_stats(
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
    body = {
        "filter": " AND ".join(filter_parts),
        "interval": {
            "startTime": request.start_time.isoformat(),
            "endTime": request.end_time.isoformat(),
        },
        "aggregation": {"perSeriesAligner": "ALIGN_MEAN", "alignmentPeriod": "60s"},
    }
    return client.list_time_series(body)
