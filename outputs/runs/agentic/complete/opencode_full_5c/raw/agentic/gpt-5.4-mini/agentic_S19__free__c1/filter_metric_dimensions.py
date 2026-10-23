from datetime import datetime
from typing import Any, Dict

from observability_client import ManagedMetricsClient
from observability_models import normalize_dimensions


def filter_metric_dimensions(
    project_id: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimensions: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    client = ManagedMetricsClient(project_id)
    dims = normalize_dimensions(dimensions)
    filter_parts = [f'metric.type="{metric_name}"']
    for key, value in dims.items():
        filter_parts.append(f'resource.labels."{key}"="{value}"')
    return client.list_time_series(
        {
            "filter": " AND ".join(filter_parts),
            "interval": {
                "startTime": start_time.isoformat(),
                "endTime": end_time.isoformat(),
            },
            "view": "FULL",
        }
    )
