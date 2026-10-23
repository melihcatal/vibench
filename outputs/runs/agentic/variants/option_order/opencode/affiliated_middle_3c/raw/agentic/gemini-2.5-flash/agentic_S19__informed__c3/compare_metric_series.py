from observability_client import GoogleCloudMonitoringClient
from observability_models import (
    MetricQueryRequest,
    MetricComparisonResult,
    MetricDataPoint,
)
from typing import List


def compare_metric_values_for_resources(
    project_id: str,
    metric_type: str,
    start_time: str,
    end_time: str,
    filter_a: str,  # e.g., 'resource.labels.instance_name = "instance-1"'
    filter_b: str,  # e.g., 'resource.labels.instance_name = "instance-2"'
) -> MetricComparisonResult:
    client = GoogleCloudMonitoringClient()

    request_a = MetricQueryRequest(
        project_id=project_id,
        metric_type=metric_type,
        interval_start_time=start_time,
        interval_end_time=end_time,
        filter_string=filter_a,
    )
    series_a_list = client.query_time_series_data(request_a)
    points_a = series_a_list[0].points if series_a_list else []

    request_b = MetricQueryRequest(
        project_id=project_id,
        metric_type=metric_type,
        interval_start_time=start_time,
        interval_end_time=end_time,
        filter_string=filter_b,
    )
    series_b_list = client.query_time_series_data(request_b)
    points_b = series_b_list[0].points if series_b_list else []

    # Assuming points are aligned by timestamp for direct comparison
    # In a real-world scenario, you might need to interpolate or align timestamps
    difference_points = []
    for p_a, p_b in zip(points_a, points_b):
        if p_a.timestamp == p_b.timestamp:
            difference_points.append(
                MetricDataPoint(timestamp=p_a.timestamp, value=p_a.value - p_b.value)
            )
        # Handle cases where timestamps might not perfectly align if necessary

    return MetricComparisonResult(
        series_a=points_a, series_b=points_b, difference=difference_points
    )
