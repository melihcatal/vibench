import time
from datetime import datetime, timedelta, timezone

from google.cloud.monitoring_v3.services.metric_service import pagers
from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricSeries, to_metric_series_list

def query_metric_window(
    project_id: str,
    metric_type: str,
    minutes_ago: int = 60,
) -> list[MetricSeries]:
    """
    Queries recent datapoints for a named metric over a time window.

    Args:
        project_id: The Google Cloud project ID.
        metric_type: The identifier of the metric, e.g., "compute.googleapis.com/instance/cpu/usage_time".
        minutes_ago: The number of minutes in the past to query.

    Returns:
        A list of MetricSeries objects containing the queried data.
    """
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {
                "seconds": seconds - (minutes_ago * 60),
                "nanos": nanos,
            },
        }
    )

    request = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results: pagers.ListTimeSeriesPager = client.list_time_series(request)
    return to_metric_series_list(results)

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment.
    # Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars.
    proj_id = get_project_id()
    # A common metric for GCE VMs. Requires a running VM to see data.
    metric = "compute.googleapis.com/instance/cpu/usage_time"
    
    print(f"Querying metric '{metric}' for project '{proj_id}' over the last 10 minutes...")
    time_series = query_metric_window(proj_id, metric, minutes_ago=10)

    if not time_series:
        print("No data found. Is the metric type correct and does the project have active resources generating it?")
    else:
        for series in time_series:
            print("--- New Time Series ---")
            print(f"Resource Labels: {series.resource_labels}")
            print(f"Metric Labels: {series.metric_labels}")
            print(f"Found {len(series.points)} points.")
            if series.points:
                print(f"  Latest point: {series.points[0].timestamp.ToDatetime()} -> {series.points[0].value}")

