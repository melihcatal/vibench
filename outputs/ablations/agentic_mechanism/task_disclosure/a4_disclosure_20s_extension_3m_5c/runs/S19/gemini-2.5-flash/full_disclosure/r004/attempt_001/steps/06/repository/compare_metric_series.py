import os
from google.cloud import monitoring_v3

def compare_metric_series(
    project_id: str,
    metric_type: str,
    time_series_1_filter: str,
    time_series_2_filter: str,
    end_time_seconds: int,
    end_time_nanos: int,
    duration_seconds: int,
):
    """Compares metric values for two resources or dimension filters over the same window.

    Args:
        project_id: Your Google Cloud Project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        time_series_1_filter: A monitoring filter for the first time series.
        time_series_2_filter: A monitoring filter for the second time series.
        end_time_seconds: The end time of the time window in seconds since epoch.
        end_time_nanos: The end time of the time window in nanoseconds.
        duration_seconds: The duration of the time window in seconds.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": end_time_seconds, "nanos": end_time_nanos},
        start_time={"seconds": end_time_seconds - duration_seconds, "nanos": end_time_nanos},
    )

    # Query for the first time series
    query_params_1 = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}" AND {time_series_1_filter}',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
    response_1 = client.list_time_series(**query_params_1)

    # Query for the second time series
    query_params_2 = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}" AND {time_series_2_filter}',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
    response_2 = client.list_time_series(**query_params_2)

    # Here you would implement your comparison logic between response_1 and response_2
    # For demonstration, we'll just print a confirmation.
    print(f"Successfully retrieved data for two time series using Google Cloud Monitoring for metric: {metric_type}")
    print(f"Time Series 1 results: {len(list(response_1.time_series))} series found.")
    print(f"Time Series 2 results: {len(list(response_2.time_series))} series found.")

    # Example of accessing data points (you'll need more sophisticated logic for actual comparison)
    # for series in response_1.time_series:
    #     for point in series.points:
    #         print(f"  Value: {point.value.double_value}, Time: {point.interval.end_time.seconds}")
    #
    # for series in response_2.time_series:
    #     for point in series.points:
    #         print(f"  Value: {point.value.double_value}, Time: {point.interval.end_time.seconds}")

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID, metric type, and filters
    # Ensure you have authenticated to Google Cloud (e.g., via gcloud auth application-default login)
    # or set GOOGLE_APPLICATION_CREDENTIALS environment variable.

    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if not project_id:
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    #     exit(1)

    # Example placeholders
    # project_id = "your-gcp-project-id"
    # metric_type = "agent.googleapis.com/agent/api_request_count"
    # time_series_1_filter = 'resource.type = "gce_instance" AND resource.labels.instance_id = "12345"'
    # time_series_2_filter = 'resource.type = "gce_instance" AND resource.labels.instance_id = "67890"'
    # end_time_seconds = 1678886400  # Example: March 15, 2023 12:00:00 PM UTC
    # end_time_nanos = 0
    # duration_seconds = 3600  # 1 hour

    # compare_metric_series(
    #     project_id,
    #     metric_type,
    #     time_series_1_filter,
    #     time_series_2_filter,
    #     end_time_seconds,
    #     end_time_nanos,
    #     duration_seconds,
    # )
    print("To use this script, uncomment the example usage block and replace with your actual values.")
    print("Ensure you have the Google Cloud Monitoring client library installed: pip install google-cloud-monitoring")
    print("And have authenticated to Google Cloud.")
