
import os
from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import MetricSeries, TimeSeriesPoint


def get_cpu_usage_for_zone(
    project_id: str, zone: str, minutes_ago: int = 20
) -> list[MetricSeries]:
    """
    Queries CPU usage for all instances within a specific GCP zone.

    Args:
        project_id: The Google Cloud project ID.
        zone: The GCP zone to filter by (e.g., 'us-central1-a').
        minutes_ago: The number of minutes in the past to query.

    Returns:
        A list of MetricSeries objects for instances in the specified zone.
    """
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.types.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )
    
    # Filter by metric type and a specific resource label (zone)
    metric_filter = (
        'metric.type = "compute.googleapis.com/instance/cpu/usage_time" AND '
        f'resource.labels.zone = "{zone}"'
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": metric_filter,
            "interval": interval,
            "view": monitoring_v3.enums.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    all_series = []
    for result in results:
        points = [
            TimeSeriesPoint(
                timestamp=point.interval.end_time.rfc3339(),
                value=point.value.double_value,
            )
            for point in result.points
        ]
        series = MetricSeries(
            name=result.metric.type,
            labels=dict(result.metric.labels),
            resource_labels=dict(result.resource.labels),
            points=points,
        )
        all_series.append(series)

    return all_series


if __name__ == "__main__":
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    target_zone = "us-central1-a"
    filtered_data = get_cpu_usage_for_zone(gcp_project_id, zone=target_zone)

    print(f"Found {len(filtered_data)} series for zone '{target_zone}'.")
    for series in filtered_data:
        instance_id = series.resource_labels.get("instance_id", "N/A")
        print(f"  Instance ID: {instance_id}")
        if series.points:
            print(f"    Latest Value: {series.points[0].value}")
