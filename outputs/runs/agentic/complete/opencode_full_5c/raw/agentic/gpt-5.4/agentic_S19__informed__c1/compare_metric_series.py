from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from observability_client import build_metric_request, get_metric_statistics
from observability_models import as_series_response


def compare_metric_series(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    left_dimensions: Dict[str, str],
    right_dimensions: Dict[str, str],
    namespace: str = "AWS/EC2",
    period: int = 300,
    stat: str = "Average",
) -> Dict[str, Any]:
    left_request = build_metric_request(
        metric_name,
        start_time,
        end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=left_dimensions,
    )
    right_request = build_metric_request(
        metric_name,
        start_time,
        end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=right_dimensions,
    )
    left_response = get_metric_statistics(left_request)
    right_response = get_metric_statistics(right_request)
    left_series = as_series_response(
        metric_name,
        namespace,
        stat,
        start_time,
        end_time,
        period,
        left_response.get("Datapoints", []),
        dimensions=left_dimensions,
        label="left",
    )
    right_series = as_series_response(
        metric_name,
        namespace,
        stat,
        start_time,
        end_time,
        period,
        right_response.get("Datapoints", []),
        dimensions=right_dimensions,
        label="right",
    )
    return {
        "provider": "amazon-cloudwatch",
        "metric": metric_name,
        "namespace": namespace,
        "left": {
            "dimensions": left_dimensions,
            "points": [point.__dict__ for point in left_series.points],
        },
        "right": {
            "dimensions": right_dimensions,
            "points": [point.__dict__ for point in right_series.points],
        },
    }
