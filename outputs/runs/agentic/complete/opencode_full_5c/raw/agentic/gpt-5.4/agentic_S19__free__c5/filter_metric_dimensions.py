from __future__ import annotations

from typing import List

from observability_models import MetricDimensionsRequest, MetricSeries, build_filter
from query_metric_window import query_metric_window


def filter_metric_dimensions(request: MetricDimensionsRequest) -> List[MetricSeries]:
    request.filter_expression = build_filter(
        metric_type=request.metric_type,
        resource_type=request.resource_type,
        metric_labels=request.metric_labels,
        resource_labels=request.resource_labels,
        extra_filter=request.filter_expression,
    )
    return query_metric_window(request)
