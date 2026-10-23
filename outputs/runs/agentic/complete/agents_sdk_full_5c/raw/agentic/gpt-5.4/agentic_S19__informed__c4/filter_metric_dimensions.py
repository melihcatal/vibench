from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from query_metric_window import query_metric_window
from observability_models import MetricWindowRequest


GOOGLE_CLOUD_MONITORING_FILTER_KEYS = ("metric.labels", "resource.labels")


def _build_dimension_filter(metric_type: str, resource_type: Optional[str], dimensions: Mapping[str, str], use_resource_labels: bool = True) -> str:
    clauses = [f'metric.type = "{metric_type}"']
    if resource_type:
        clauses.append(f'resource.type = "{resource_type}"')
    prefix = "resource.labels" if use_resource_labels else "metric.labels"
    for key, value in dimensions.items():
        clauses.append(f'{prefix}.{key} = "{value}"')
    return " AND ".join(clauses)


def filter_metric_dimensions(project_id: str, metric_type: str, dimensions: Mapping[str, str], minutes: int = 15, resource_type: Optional[str] = None, use_resource_labels: bool = True) -> Dict[str, Any]:
    request = MetricWindowRequest(
        project_id=project_id,
        metric_type=metric_type,
        minutes=minutes,
        resource_type=resource_type,
        filter_expression=_build_dimension_filter(metric_type, resource_type, dimensions, use_resource_labels=use_resource_labels),
    )
    return query_metric_window(request)
