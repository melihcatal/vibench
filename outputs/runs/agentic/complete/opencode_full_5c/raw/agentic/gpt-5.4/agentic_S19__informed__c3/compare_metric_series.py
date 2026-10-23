from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, Optional

from observability_client import get_cloudwatch_client
from observability_models import ComparisonResponse, Datapoint, normalize_dimensions


def compare_metric_series(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    left_dimensions: Optional[Dict[str, Any]],
    right_dimensions: Optional[Dict[str, Any]],
    period: int = 60,
    stat: str = "Average",
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_cloudwatch_client(region_name=region_name)
    left_dims = normalize_dimensions(left_dimensions)
    right_dims = normalize_dimensions(right_dimensions)
    queries = [
        client.build_metric_data_query(
            "leftseries", namespace, metric_name, left_dims, stat, period, "left"
        ),
        client.build_metric_data_query(
            "rightseries", namespace, metric_name, right_dims, stat, period, "right"
        ),
    ]
    response = client.get_metric_data(
        namespace, metric_name, start_time, end_time, queries
    )
    results = {item["Id"]: item for item in response.get("MetricDataResults", [])}

    def build_points(result_id: str, dims: Dict[str, str]) -> list[Datapoint]:
        result = results.get(result_id, {})
        timestamps = result.get("Timestamps", [])
        values = result.get("Values", [])
        ordered = sorted(zip(timestamps, values), key=lambda pair: pair[0])
        return [
            Datapoint(
                timestamp=ts.isoformat(), value=float(val), stat=stat, dimensions=dims
            )
            for ts, val in ordered
        ]

    left_points = build_points("leftseries", left_dims)
    right_points = build_points("rightseries", right_dims)
    left_latest = left_points[-1].value if left_points else None
    right_latest = right_points[-1].value if right_points else None
    delta = (
        (left_latest - right_latest)
        if left_latest is not None and right_latest is not None
        else None
    )
    ratio = (
        (left_latest / right_latest)
        if left_latest is not None and right_latest not in (None, 0)
        else None
    )
    return asdict(
        ComparisonResponse(
            provider=client.provider,
            metric_name=metric_name,
            left_dimensions=left_dims,
            right_dimensions=right_dims,
            left_latest=left_latest,
            right_latest=right_latest,
            delta=delta,
            ratio=ratio,
            left_points=left_points,
            right_points=right_points,
        )
    )
