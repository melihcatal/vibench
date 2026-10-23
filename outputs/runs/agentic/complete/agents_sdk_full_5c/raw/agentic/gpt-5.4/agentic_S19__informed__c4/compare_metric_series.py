from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from filter_metric_dimensions import _build_dimension_filter
from query_metric_window import query_metric_window
from observability_models import MetricComparisonResponse, MetricSeries, MetricWindowRequest


GOOGLE_CLOUD_COMPARISON_PROVIDER = "Google Cloud Monitoring"


def _first_series(payload: Dict[str, Any]) -> MetricSeries:
    raw = (payload.get("series") or [])[0]
    return MetricSeries(**raw)


def compare_metric_series(project_id: str, metric_type: str, left_dimensions: Mapping[str, str], right_dimensions: Mapping[str, str], minutes: int = 15, resource_type: Optional[str] = None) -> Dict[str, Any]:
    left_payload = query_metric_window(MetricWindowRequest(project_id=project_id, metric_type=metric_type, minutes=minutes, resource_type=resource_type, filter_expression=_build_dimension_filter(metric_type, resource_type, left_dimensions)))
    right_payload = query_metric_window(MetricWindowRequest(project_id=project_id, metric_type=metric_type, minutes=minutes, resource_type=resource_type, filter_expression=_build_dimension_filter(metric_type, resource_type, right_dimensions)))

    left_series = _first_series(left_payload)
    right_series = _first_series(right_payload)
    deltas = []
    for left_point, right_point in zip(left_series.points, right_series.points):
        left_value = left_point.get("value") if isinstance(left_point, dict) else None
        right_value = right_point.get("value") if isinstance(right_point, dict) else None
        deltas.append(
            {
                "interval_end": (left_point.get("interval_end") if isinstance(left_point, dict) else None) or (right_point.get("interval_end") if isinstance(right_point, dict) else None),
                "left_value": left_value,
                "right_value": right_value,
                "difference": (left_value - right_value) if left_value is not None and right_value is not None else None,
            }
        )
    response = MetricComparisonResponse(left=left_series, right=right_series, deltas=deltas)
    return {"provider": GOOGLE_CLOUD_COMPARISON_PROVIDER, "left": response.left.__dict__, "right": response.right.__dict__, "deltas": response.deltas}
