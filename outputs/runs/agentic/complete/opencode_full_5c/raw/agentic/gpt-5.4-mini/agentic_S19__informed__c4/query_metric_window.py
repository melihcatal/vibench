from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from observability_client import datadog_get
from observability_models import MetricWindowRequest, extract_series_points


def query_metric_window(
    metric: str,
    start: datetime,
    end: datetime,
    dimensions: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    request = MetricWindowRequest(
        metric=metric, start=start, end=end, dimensions=dimensions
    )
    payload = datadog_get(f"/api/v1/query/{metric}", params=request.to_params())
    return {"metric": metric, "points": extract_series_points(payload), "raw": payload}
