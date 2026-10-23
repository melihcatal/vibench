
import os
from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import MetricSeries, TimeSeriesPoint


def get_aggregated_cpu_usage(
    project_id: str, minutes_ago: int = 60
) -> list[MetricSeries]:
    """
    Queries aggregated 'compute.googleapis.com/instance/cpu/utilization' metric.

    This function gets the mean CPU utilization across all instances, aligned
    to a 5-minute interval.

    Args:
        project_id: The Google Cloud project ID.
        minutes_ago: The number of minutes in the past to query.

    Returns:
        A list of MetricSeries objects containing the aggregated data.
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

    aggregation = monitoring_v3.types.Aggregation(
        {
            "alignment_period": {"seconds": 300},  # 5 minutes
            "per_series_aligner": monitoring_v3.enums.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.enums.Aggregation.Reducer.REDUCE_MEAN,
            "group_by_fields": ["metric.label.\"instance_name\""],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.enums.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
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

    aggregated_data = get_aggregated_cpu_usage(gcp_project_id, minutes_ago=30)
    print(f"Found {len(aggregated_data)} aggregated time series.")
    for series in aggregated_data:
        print(f"  Instance Name: {series.labels.get('instance_name', 'N/A')}")
        if series.points:
            print(f"    Latest mean value: {series.points[0].value:.4f}")

