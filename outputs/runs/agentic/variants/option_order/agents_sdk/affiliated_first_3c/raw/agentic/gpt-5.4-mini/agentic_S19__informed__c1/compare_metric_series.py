from __future__ import annotations

from dataclasses import dataclass

from observability_models import MetricComparisonResponse, MetricSeriesResponse, MetricWindowRequest
from query_metric_window import query_metric_window


@dataclass(frozen=True)
class ComparisonRequest:
    left: MetricWindowRequest
    right: MetricWindowRequest


def compare_metric_series(request: ComparisonRequest) -> MetricComparisonResponse:
    left = query_metric_window(request.left)
    right = query_metric_window(request.right)
    return MetricComparisonResponse(left=left, right=right)
