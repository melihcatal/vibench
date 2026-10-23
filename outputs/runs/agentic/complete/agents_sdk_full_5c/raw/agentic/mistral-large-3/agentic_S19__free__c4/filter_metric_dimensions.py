from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricDataPoint, MetricQueryRequest


def filter_metric_dimensions(
    metric_type: str, dimension_filters: dict[str, str], hours: int = 1
) -> list[MetricDataPoint]:
    """Query metric data filtered by resource labels or dimensions using Google Cloud Monitoring."""
    client = get_monitoring_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    filter_parts = [f'metric.type="{metric_type}"']
    for key, value in dimension_filters.items():
        filter_parts.append(f'resource.label.{key}="{value}"')

    query_request = {
        "name": f"projects/{project_id}",
        "filter": " AND ".join(filter_parts),
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())},
        },
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    time_series = client.list_time_series(request=query_request)
    datapoints = []

    for series in time_series:
        for point in series.points:
            datapoints.append(
                MetricDataPoint(
                    timestamp=point.interval.end_time.timestamp(),
                    value=float(point.value.double_value),
                    labels=dict(series.resource.labels),
                )
            )

    return datapoints