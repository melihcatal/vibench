from __future__ import annotations

from typing import Mapping

from observability_models import MetricComparisonResponse, MetricSeriesResponse, MetricWindowRequest
from query_metric_window import query_metric_window


def compare_metric_series(left_request: MetricWindowRequest, right_request: MetricWindowRequest) -> MetricComparisonResponse:
    left = query_metric_window(left_request)
    right = query_metric_window(right_request)
    return MetricComparisonResponse(metric_name=left_request.metric_name, left=left, right=right)
