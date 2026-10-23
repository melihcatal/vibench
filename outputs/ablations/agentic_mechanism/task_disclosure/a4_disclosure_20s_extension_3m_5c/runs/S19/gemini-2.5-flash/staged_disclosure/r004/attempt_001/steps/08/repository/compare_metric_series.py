
from google.cloud import monitoring_v3

def compare_metric_series(project_id: str, metric_type: str, filter1: str, filter2: str, interval_start_time, interval_end_time):
    """Compares metric values for two resources or dimension filters over the same window.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        filter1: The monitoring filter for the first resource/dimension.
        filter2: The monitoring filter for the second resource/dimension.
        interval_start_time: The start time for the metric data (RFC3339 format).
        interval_end_time: The end time for the metric data (RFC3339 format).
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Query for the first series
    series1 = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter1,
            "interval": {
                "start_time": {"seconds": interval_start_time.timestamp()},
                "end_time": {"seconds": interval_end_time.timestamp()},
            },
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "metric_kind": monitoring_v3.MetricKind.GAUGE,
        }
    )

    # Query for the second series
    series2 = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter2,
            "interval": {
                "start_time": {"seconds": interval_start_time.timestamp()},
                "end_time": {"seconds": interval_end_time.timestamp()},
            },
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "metric_kind": monitoring_v3.MetricKind.GAUGE,
        }
    )

    print(f"Metric Series 1 for filter: {filter1}")
    for ts in series1:
        print(ts)

    print(f"\nMetric Series 2 for filter: {filter2}")
    for ts in series2:
        print(ts)

    # Further comparison logic would go here, e.g., calculating differences, averages, etc.

if __name__ == '__main__':
    # Example usage (replace with your actual project ID, metric, and filters)
    import datetime
    project_id = "YOUR_PROJECT_ID"  # Replace with your Google Cloud Project ID
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    # Example filters - replace with your actual filters
    # For instance, you might filter by resource labels or monitored resource types
    filter_instance1 = f'metric.type="{metric_type}" AND resource.type="gce_instance" AND resource.labels.instance_id="INSTANCE_ID_1"'
    filter_instance2 = f'metric.type="{metric_type}" AND resource.type="gce_instance" AND resource.labels.instance_id="INSTANCE_ID_2"'

    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(hours=1)

    # For demonstration, let's use a generic filter for two different zones
    filter_zone1 = f'metric.type="{metric_type}" AND resource.type="gce_instance" AND resource.labels.zone="us-central1-a"'
    filter_zone2 = f'metric.type="{metric_type}" AND resource.type="gce_instance" AND resource.labels.zone="us-central1-c"'

    print("Comparing CPU utilization for two different zones:")
    compare_metric_series(project_id, metric_type, filter_zone1, filter_zone2, start_time, end_time)
