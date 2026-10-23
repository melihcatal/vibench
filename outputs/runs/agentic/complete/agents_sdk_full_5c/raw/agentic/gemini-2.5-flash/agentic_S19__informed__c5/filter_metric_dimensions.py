from datetime import datetime, timedelta, timezone
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricQueryRequest, MetricQueryResponse, TimeSeries, TimeSeriesPoint

def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int,
    dimension_filter: str,
) -> MetricQueryResponse:
    """Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring.

    Args:
        project_id: The Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time: The end of the time window.
        duration_minutes: The duration of the window in minutes.
        dimension_filter: A Monitoring filter string (e.g., 'resource.labels.instance_name = "my-instance"').

    Returns:
        A MetricQueryResponse containing the filtered time series data.
    """
    client = get_monitoring_client()

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())},
    )

    query_filter = f'metric.type = "{metric_type}" AND {dimension_filter}'

    time_series_list = []
    for ts in client.list_time_series(
        name=f"projects/{project_id}",
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    ):
        points = [
            TimeSeriesPoint(value=p.value.double_value if p.value.WhichOneof("value") == "double_value" else p.value.int64_value,
                            timestamp=p.interval.end_time.isoformat())
            for p in ts.points
        ]
        time_series_list.append(
            TimeSeries(
                metric_type=ts.metric.type,
                resource_labels=dict(ts.resource.labels),
                metric_labels=dict(ts.metric.labels),
                points=points,
            )
        )

    return MetricQueryResponse(time_series=time_series_list)

if __name__ == '__main__':
    project = get_project_id()
    if project:
        # Example: Query CPU utilization for a specific instance
        current_time = datetime.now(timezone.utc)
        metric = "compute.googleapis.com/instance/cpu/utilization"
        # Replace with a real instance name or label that exists in your project
        instance_filter = 'resource.labels.instance_name = "your-instance-name"' # Placeholder
        print(f"Querying {metric} for project {project} filtered by \'{instance_filter}\'...")
        print("Note: You will likely need to adjust the \'instance_filter\' variable to a valid instance in your GCP project.")
        response = filter_metric_dimensions(project, metric, current_time, 60, instance_filter)
        if response.time_series:
            print(f"Found {len(response.time_series)} filtered time series.")
            for i, ts in enumerate(response.time_series[:2]):
                print(f"Series {i+1} (Metric: {ts.metric_type}, Resource: {ts.resource_labels}): {len(ts.points)} points.")
        else:
            print("No filtered time series data found. Check your instance name or filter.")
    else:
        print("Error: Google Cloud project ID not found. Set GOOGLE_CLOUD_PROJECT or GCP_PROJECT environment variable.")
