from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from observability_client import build_metric_request, get_metric_statistics
from observability_models import as_series_response


def filter_metric_dimensions(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimensions: Dict[str, str],
    namespace: str = "AWS/EC2",
    period: int = 300,
    stat: str = "Average",
) -> Dict[str, Any]:
    request = build_metric_request(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=dimensions,
    )
    response = get_metric_statistics(request)
    series = as_series_response(
        metric_name=metric_name,
        namespace=namespace,
        stat=stat,
        start_time=start_time,
        end_time=end_time,
        period=period,
        datapoints=response.get("Datapoints", []),
        dimensions=dimensions,
        label=response.get("Label"),
    )
    return {
        "provider": "amazon-cloudwatch",
        "dimension_filter": dimensions,
        "metric": series.metric_name,
        "namespace": series.namespace,
        "points": [point.__dict__ for point in series.points],
    }
