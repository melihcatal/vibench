from datetime import datetime, timedelta, timezone
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricQueryRequest, MetricQueryResponse, TimeSeries, TimeSeriesPoint

def query_metric_window(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int,
) -> MetricQueryResponse:
    """Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: The Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time: The end of the time window.
        duration_minutes: The duration of the window in minutes.

    Returns:
        A MetricQueryResponse containing the time series data.
    """
    client = get_monitoring_client()

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())},
    )

    query_filter = f'metric.type = "{metric_type}"'

    time_series_list = []
    for ts in client.list_time_series(
        name=f"projects/{project_id}",
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    ):
        points = [
            TimeSeriesPoint(value=p.value.double_value if p.value.WhichOneof("value") == "double_value" else p.value.int6_value,
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
        # Example: Query CPU utilization for the last 60 minutes
        current_time = datetime.now(timezone.utc)
        metric = "compute.googleapis.com/instance/cpu/utilization"
        print(f"Querying {metric} for project {project} for the last 60 minutes...")
        response = query_metric_window(project, metric, current_time, 60)
        if response.time_series:
            print(f"Found {len(response.time_series)} time series.")
            for i, ts in enumerate(response.time_series[:2]): # Print first 2 for brevity
                print(f"Series {i+1} (Metric: {ts.metric_type}, Resource: {ts.resource_labels}): {len(ts.points)} points.")
        else:
            print("No time series data found.")
    else:
        print("Error: Google Cloud project ID not found. Set GOOGLE_CLOUD_PROJECT or GCP_PROJECT environment variable.")
