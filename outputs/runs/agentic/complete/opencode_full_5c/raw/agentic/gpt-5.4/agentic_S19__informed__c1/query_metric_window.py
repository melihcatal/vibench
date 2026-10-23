from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from observability_client import build_metric_request, get_metric_statistics
from observability_models import as_series_response


def query_metric_window(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    namespace: str = "AWS/EC2",
    period: int = 300,
    stat: str = "Average",
    dimensions: Optional[Dict[str, str]] = None,
    unit: Optional[str] = None,
) -> Dict[str, Any]:
    request = build_metric_request(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=dimensions,
        unit=unit,
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
    )
    return {
        "provider": "amazon-cloudwatch",
        "region": response.get("Label") and None,
        "metric": series.metric_name,
        "namespace": series.namespace,
        "stat": series.stat,
        "start_time": series.start_time,
        "end_time": series.end_time,
        "period": series.period,
        "label": response.get("Label"),
        "points": [point.__dict__ for point in series.points],
    }
