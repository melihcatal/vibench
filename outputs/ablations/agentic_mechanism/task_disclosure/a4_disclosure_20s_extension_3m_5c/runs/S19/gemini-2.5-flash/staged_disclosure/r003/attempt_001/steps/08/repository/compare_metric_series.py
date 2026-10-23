import os
from google.cloud import monitoring_v3

def compare_metric_series(project_id: str,
                          metric_type: str,
                          filter1: str,
                          filter2: str,
                          end_time_seconds: int,
                          duration_seconds: int):
    """Compares metric values for two resources or dimension filters over the same window.

    Args:
        project_id: Your Google Cloud Project ID.
        metric_type: The metric type to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        filter1: The monitoring filter for the first series (e.g., 'metric.labels.instance_name="my-instance-1"').
        filter2: The monitoring filter for the second series (e.g., 'metric.labels.instance_name="my-instance-2"').
        end_time_seconds: The end time of the time series in Unix timestamp seconds.
        duration_seconds: The duration of the time series in seconds.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': end_time_seconds},
        start_time={'seconds': end_time_seconds - duration_seconds}
    )

    # Fetch data for the first filter
    query_filter1 = f'metric.type = "{metric_type}" AND resource.type = "gce_instance" AND {filter1}'
    series1 = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter1,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    print(f"Series 1 data:")
    for ts in series1:
        print(ts)

    # Fetch data for the second filter
    query_filter2 = f'metric.type = "{metric_type}" AND resource.type = "gce_instance" AND {filter2}'
    series2 = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter2,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    print(f"Series 2 data:")
    for ts in series2:
        print(ts)

    # Placeholder for comparison logic
    print("\nComparison logic would go here.")

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and metric details)
    # Ensure you have GOOGLE_APPLICATION_CREDENTIALS set or are authenticated
    # via gcloud login
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    filter1 = 'metric.labels.instance_name="instance-1"' # Example filter
    filter2 = 'metric.labels.instance_name="instance-2"' # Example filter
    
    import time
    end_time = int(time.time())
    duration = 3600 # 1 hour

    compare_metric_series(project_id, metric_type, filter1, filter2, end_time, duration)
