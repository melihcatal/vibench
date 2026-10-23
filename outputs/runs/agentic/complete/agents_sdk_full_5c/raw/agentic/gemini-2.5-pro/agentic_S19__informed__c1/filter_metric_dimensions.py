import time
from typing import Dict
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricSeries, to_metric_series_list

def query_with_dimension_filters(
    project_id: str,
    metric_type: str,
    filter_dimensions: Dict[str, str],
    minutes_ago: int = 60,
) -> list[MetricSeries]:
    """
    Queries metric data filtered by resource labels or dimensions.

    Args:
        project_id: The Google Cloud project ID.
        metric_type: The identifier of the metric.
        filter_dimensions: A dictionary of labels to filter by, e.g.,
                           {'resource.labels.instance_id': '12345'}.
        minutes_ago: The time window in minutes.

    Returns:
        A list of matching MetricSeries objects.
    """
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": seconds - (minutes_ago * 60), "nanos": nanos},
        }
    )

    dimension_filters = " AND ".join(
        [f'{key} = "{value}"' for key, value in filter_dimensions.items()]
    )
    
    full_filter = f'metric.type = "{metric_type}" AND {dimension_filters}'

    request = {
        "name": project_name,
        "filter": full_filter,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results = client.list_time_series(request)
    return to_metric_series_list(results)

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment.
    proj_id = get_project_id()
    metric = "compute.googleapis.com/instance/cpu/usage_time"
    # Replace with a real instance ID and zone from your project.
    filters = {
        "resource.labels.instance_id": "your-instance-id-here",
        "resource.labels.zone": "us-central1-a" 
    }
    
    print(f"Querying metric '{metric}' with filters: {filters}...")
    try:
        filtered_series = query_with_dimension_filters(proj_id, metric, filters, minutes_ago=20)
        
        if not filtered_series:
            print("No data found. Check your filters and if the resource is active.")
        else:
            for series in filtered_series:
                print("--- Filtered Time Series ---")
                print(f"Resource Labels: {series.resource_labels}")
                if series.points:
                    print(f"  Latest point value: {series.points[0].value}")

    except ValueError as e:
        print(f"Error: {e}. Did you replace the placeholder filter values?")

