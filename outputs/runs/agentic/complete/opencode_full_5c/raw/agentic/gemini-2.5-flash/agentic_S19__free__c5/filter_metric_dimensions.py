import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    minutes: int = 5,
    resource_label_key: str = None,
    resource_label_value: str = None,
):
    """Queries metric data filtered by resource labels or dimensions."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    query_filter = f'metric.type="{metric_type}"'
    if resource_label_key and resource_label_value:
        query_filter += (
            f' AND resource.labels.{resource_label_key}="{resource_label_value}"'
        )

    query = (
        f'fetchTimeSeries({project_name}, "{query_filter}")'
        f' | within(start_time="{start_time.isoformat()}Z", end_time="{end_time.isoformat()}Z")'
    )

    results = client.query_time_series(
        name=project_name,
        query=query,
    )

    return results
