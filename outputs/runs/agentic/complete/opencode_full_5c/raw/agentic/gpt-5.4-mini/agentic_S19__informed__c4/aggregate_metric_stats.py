from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from observability_client import datadog_get
from observability_models import MetricWindowRequest, extract_statistics


def aggregate_metric_stats(
    metric: str,
    start: datetime,
    end: datetime,
    dimensions: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    request = MetricWindowRequest(
        metric=metric, start=start, end=end, dimensions=dimensions
    )
    payload = datadog_get(f"/api/v1/query/{metric}/stats", params=request.to_params())
    return {"metric": metric, "statistics": extract_statistics(payload), "raw": payload}
