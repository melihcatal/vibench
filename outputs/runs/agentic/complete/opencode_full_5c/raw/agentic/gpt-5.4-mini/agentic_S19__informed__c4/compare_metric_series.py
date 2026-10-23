from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from observability_client import datadog_get
from observability_models import MetricWindowRequest, extract_series_points


def compare_metric_series(
    metric: str,
    start: datetime,
    end: datetime,
    left_dimensions: Dict[str, str],
    right_dimensions: Dict[str, str],
) -> Dict[str, Any]:
    left = MetricWindowRequest(
        metric=metric, start=start, end=end, dimensions=left_dimensions
    )
    right = MetricWindowRequest(
        metric=metric, start=start, end=end, dimensions=right_dimensions
    )
    left_payload = datadog_get(
        f"/api/v1/query/{metric}/compare/left", params=left.to_params()
    )
    right_payload = datadog_get(
        f"/api/v1/query/{metric}/compare/right", params=right.to_params()
    )
    return {
        "metric": metric,
        "left": extract_series_points(left_payload),
        "right": extract_series_points(right_payload),
        "raw": {"left": left_payload, "right": right_payload},
    }
