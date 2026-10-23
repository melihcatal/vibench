from datetime import datetime, timedelta, timezone
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricQueryResponse

def compare_metric_series(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int,
    filter1: str,
    filter2: str,
) -> tuple[MetricQueryResponse, MetricQueryResponse]:
    """Compares metric values for two resources or dimension filters over the same window
    using Google Cloud Monitoring.

    Args:
        project_id: The Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time: The end of the time window.
        duration_minutes: The duration of the window in minutes.
        filter1: The first Monitoring filter string.
        filter2: The second Monitoring filter string.

    Returns:
        A tuple containing two MetricQueryResponse objects, one for each filter.
    """
    client = get_monitoring_client()

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())},
    )

    def _query_series(f: str) -> MetricQueryResponse:
        query_filter = f'metric.type = "{metric_type}" AND {f}'
        time_series_list = []
        for ts in client.list_time_series(
            name=f"projects/{project_id}",
            filter=query_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        ):
            points = [
                {
                    "value": p.value.double_value if p.value.WhichOneof("value") == "double_value" else p.value.int64_value,
                    "timestamp": p.interval.end_time.isoformat()
                }
                for p in ts.points
            ]
            time_series_list.append({
                "metric_type": ts.metric.type,
                "resource_labels": dict(ts.resource.labels),
                "metric_labels": dict(ts.metric.labels),
                "points": points,
            })
        return MetricQueryResponse(time_series=time_series_list)

    response1 = _query_series(filter1)
    response2 = _query_series(filter2)

    return response1, response2

if __name__ == '__main__':
    project = get_project_id()
    if project:
        current_time = datetime.now(timezone.utc)
        metric = "compute.googleapis.com/instance/cpu/utilization"

        # Replace with real instance names or labels from your project
        filter_a = 'resource.labels.instance_name = "instance-a"' # Placeholder
        filter_b = 'resource.labels.instance_name = "instance-b"' # Placeholder
        print(f"Comparing {metric} for project {project} between \'{filter_a}\' and \'{filter_b}\' over last 60 minutes...")
        print("Note: You will likely need to adjust the \'filter_a\' and \'filter_b\' variables to valid instances in your GCP project.")

        response_a, response_b = compare_metric_series(
            project, metric, current_time, 60, filter_a, filter_b
        )

        print(f"Results for Filter A ({filter_a}): {len(response_a.time_series)} series found.")
        if response_a.time_series:
            for i, ts in enumerate(response_a.time_series[:1]):
                print(f"  Series {i+1} (Points: {len(ts.points)}) Ex: {ts.points[0]['value']} at {ts.points[0]['timestamp']}")

        print(f"Results for Filter B ({filter_b}): {len(response_b.time_series)} series found.")
        if response_b.time_series:
            for i, ts in enumerate(response_b.time_series[:1]):
                print(f"  Series {i+1} (Points: {len(ts.points)}) Ex: {ts.points[0]['value']} at {ts.points[0]['timestamp']}")

    else:
        print("Error: Google Cloud project ID not found. Set GOOGLE_CLOUD_PROJECT or GCP_PROJECT environment variable.")
