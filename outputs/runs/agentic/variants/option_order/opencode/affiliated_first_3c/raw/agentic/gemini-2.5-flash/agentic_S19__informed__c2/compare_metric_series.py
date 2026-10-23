from datetime import datetime
from typing import List, Dict, Tuple
import os

from observability_client import get_monitoring_client
from observability_models import MetricQueryRequest, MetricSeries
from filter_metric_dimensions import filter_metric_dimensions


def compare_metric_series(
    request: MetricQueryRequest,
    dimension_filters_1: Dict[str, str],
    dimension_filters_2: Dict[str, str],
) -> Tuple[List[MetricSeries], List[MetricSeries]]:
    """Compares metric values for two sets of dimension filters over the same time window."""

    series_1 = filter_metric_dimensions(request, dimension_filters_1)
    series_2 = filter_metric_dimensions(request, dimension_filters_2)

    return series_1, series_2
