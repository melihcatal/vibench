import os
from datetime import datetime, timedelta

from google.cloud import monitoring_v3

def compare_metric_series(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int,
    filter_set_1: dict, # e.g., {'instance_name': 'my-instance-1'}
    filter_set_2: dict, # e.g., {'instance_name': 'my-instance-2'}
):
    """Compares metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())},
    )

    def _build_filter(metric_type, dimension_filters):
        filter_parts = [f'metric.type = "{metric_type}"']
        for dim, value in dimension_filters.items():
            filter_parts.append(f'resource.labels.\"{dim}\" = "{value}"')
        return " AND ".join(filter_parts)

    query_filter_1 = _build_filter(metric_type, filter_set_1)
    query_filter_2 = _build_filter(metric_type, filter_set_2)

    series_1 = client.list_time_series(
        name=project_name,
        filter=query_filter_1,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    series_2 = client.list_time_series(
        name=project_name,
        filter=query_filter_2,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return {'series_1': list(series_1), 'series_2': list(series_2)}
