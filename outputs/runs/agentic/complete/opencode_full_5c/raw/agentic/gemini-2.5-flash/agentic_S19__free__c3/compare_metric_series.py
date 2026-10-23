import os
from datetime import datetime
from typing import Dict, List
from observability_models import MetricComparison, TimeSeriesData
from filter_metric_dimensions import filter_metric_dimensions


def compare_metric_series(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    start_time: datetime,
    resource_labels_a: Dict[str, str],
    resource_labels_b: Dict[str, str],
) -> MetricComparison:
    # Fetch data for series A
    series_a_data = filter_metric_dimensions(
        project_id=project_id,
        metric_type=metric_type,
        end_time=end_time,
        start_time=start_time,
        resource_labels=resource_labels_a,
    )

    # Fetch data for series B
    series_b_data = filter_metric_dimensions(
        project_id=project_id,
        metric_type=metric_type,
        end_time=end_time,
        start_time=start_time,
        resource_labels=resource_labels_b,
    )

    # For simplicity, we assume there's at most one TimeSeriesData object per filter.
    # In a real scenario, you might need to combine or select a specific series if multiple match.
    series_a_single = (
        series_a_data[0]
        if series_a_data
        else TimeSeriesData(
            metric_type=metric_type, resource_labels=resource_labels_a, points=[]
        )
    )
    series_b_single = (
        series_b_data[0]
        if series_b_data
        else TimeSeriesData(
            metric_type=metric_type, resource_labels=resource_labels_b, points=[]
        )
    )

    return MetricComparison(
        metric_type=metric_type,
        series_a=series_a_single,
        series_b=series_b_single,
    )
