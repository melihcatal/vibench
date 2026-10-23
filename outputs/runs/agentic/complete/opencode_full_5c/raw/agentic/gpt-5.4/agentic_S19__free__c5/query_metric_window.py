from __future__ import annotations

from typing import List

from observability_client import fetch_time_series
from observability_models import (
    MetricPoint,
    MetricSeries,
    MetricWindowRequest,
    build_filter,
    normalize_numeric_typed_value,
)


def query_metric_window(request: MetricWindowRequest) -> List[MetricSeries]:
    filter_expression = request.filter_expression or build_filter(request.metric_type)
    payload = fetch_time_series(
        filter_expression=filter_expression,
        start_time=request.start_rfc3339(),
        end_time=request.end_rfc3339(),
        project_id=request.project_id,
        alignment_period_seconds=request.alignment_period_seconds,
        per_series_aligner=request.per_series_aligner,
        view=request.view,
    )
    results: List[MetricSeries] = []
    for series in payload.get("timeSeries", []):
        points = []
        for point in series.get("points", []):
            value = normalize_numeric_typed_value(point.get("value", {}))
            if value is None:
                continue
            points.append(
                MetricPoint(
                    series_name=series.get("metric", {}).get(
                        "type", request.metric_type
                    ),
                    timestamp=point.get("interval", {}).get("endTime", ""),
                    value=value,
                    unit=series.get("unit"),
                    metric_labels=series.get("metric", {}).get("labels", {}),
                    resource_labels=series.get("resource", {}).get("labels", {}),
                )
            )
        results.append(
            MetricSeries(
                series_name=series.get("metric", {}).get("type", request.metric_type),
                metric_type=series.get("metric", {}).get("type", request.metric_type),
                resource_type=series.get("resource", {}).get("type"),
                metric_labels=series.get("metric", {}).get("labels", {}),
                resource_labels=series.get("resource", {}).get("labels", {}),
                points=points,
            )
        )
    return results
