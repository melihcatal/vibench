import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3


def compare_metric_series(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    minutes: int = 60,
    filter_a: str = None,  # Example: 'resource.labels.instance_name="instance-1"'
    filter_b: str = None,  # Example: 'resource.labels.instance_name="instance-2"'
):
    """Compares metric values for two resources or dimension filters over the same window."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    # Query for series A
    query_a = (
        f'fetchTimeSeries({project_name}, "metric.type="{metric_type}" AND {filter_a}")'
        f' | within(start_time="{start_time.isoformat()}Z", end_time="{end_time.isoformat()}Z")'
    )
    results_a = client.query_time_series(name=project_name, query=query_a)

    # Query for series B
    query_b = (
        f'fetchTimeSeries({project_name}, "metric.type="{metric_type}" AND {filter_b}")'
        f' | within(start_time="{start_time.isoformat()}Z", end_time="{end_time.isoformat()}Z")'
    )
    results_b = client.query_time_series(name=project_name, query=query_b)

    return {"series_a": results_a, "series_b": results_b}
