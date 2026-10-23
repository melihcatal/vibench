from datetime import datetime
from typing import Any, Dict

from observability_client import ManagedMetricsClient
from observability_models import MetricSeriesComparisonRequest, normalize_dimensions


def compare_metric_series(
    project_id: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    left_dimensions: Dict[str, Any] | None = None,
    right_dimensions: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    client = ManagedMetricsClient(project_id)
    request = MetricSeriesComparisonRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        left_dimensions=normalize_dimensions(left_dimensions),
        right_dimensions=normalize_dimensions(right_dimensions),
    )

    def build_filter(dimensions):
        parts = [f'metric.type="{request.metric_name}"']
        for key, value in dimensions.items():
            parts.append(f'resource.labels."{key}"="{value}"')
        return " AND ".join(parts)

    left = client.list_time_series(
        {
            "filter": build_filter(request.left_dimensions or {}),
            "interval": {
                "startTime": request.start_time.isoformat(),
                "endTime": request.end_time.isoformat(),
            },
            "view": "FULL",
        }
    )
    right = client.list_time_series(
        {
            "filter": build_filter(request.right_dimensions or {}),
            "interval": {
                "startTime": request.start_time.isoformat(),
                "endTime": request.end_time.isoformat(),
            },
            "view": "FULL",
        }
    )
    return {"left": left, "right": right}
