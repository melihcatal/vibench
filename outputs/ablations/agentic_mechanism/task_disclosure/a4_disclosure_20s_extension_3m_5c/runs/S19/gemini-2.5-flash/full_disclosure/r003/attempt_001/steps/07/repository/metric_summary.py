import os
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import time

def summarize_metric_anomalies(project_id: str, metric_type: str, lookback_minutes: int = 60):
    """
    Summarizes recent metric trends or anomalies using Google Cloud Monitoring.

    Args:
        project_id: The Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        lookback_minutes: The number of minutes to look back for data.

    Returns:
        A string summarizing the metric trends or anomalies.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": seconds, "nanos": nanos},
        start_time={"seconds": seconds - (lookback_minutes * 60), "nanos": nanos},
    )

    query_filter = f'metric.type = "{metric_type}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    response = client.list_time_series(request=request)

    summary_data = []
    for series in response:
        for point in series.points:
            summary_data.append(point.value.double_value) # Assuming double value metrics for simplicity

    if not summary_data:
        return f"No data found for metric {metric_type} in the last {lookback_minutes} minutes."

    # Placeholder for actual anomaly detection or trend summarization logic
    # In a real scenario, you would analyze 'summary_data' to find anomalies,
    # calculate trends (e.g., average, min, max, std dev), etc.
    avg_value = sum(summary_data) / len(summary_data)
    min_value = min(summary_data)
    max_value = max(summary_data)

    return (
        f"Summary for metric '{metric_type}' over the last {lookback_minutes} minutes:\n"
        f"  - Average value: {avg_value:.2f}\n"
        f"  - Minimum value: {min_value:.2f}\n"
        f"  - Maximum value: {max_value:.2f}\n"
        f"  (Further anomaly detection or trend analysis would be implemented here.)"
    )

if __name__ == "__main__":
    # Example Usage (replace with your actual project_id and metric_type)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # gcloud is configured with appropriate authentication.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    METRIC_TYPE = "compute.googleapis.com/instance/cpu/utilization" # Example metric
    LOOKBACK = 30 # minutes

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or update the PROJECT_ID in the script.")
    else:
        summary = summarize_metric_anomalies(PROJECT_ID, METRIC_TYPE, LOOKBACK)
        print(summary)
