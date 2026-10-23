from google.cloud import monitoring_v3
from google.api_core import datetime_helpers
from datetime import datetime, timedelta

def query_metric_window(project_id: str, metric_type: str, window_minutes: int):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    interval = monitoring_v3.TimeInterval(
        end_time=datetime_helpers.to_rfc3339(now),
        start_time=datetime_helpers.to_rfc3339(now - timedelta(minutes=window_minutes)),
    )

    query = f"""
        fetch gce_instance
        | metric {metric_type}
        | within {window_minutes}m
        | group_by [], [value_max: max(value)]
    """

    results = client.query_time_series(
        request={
            "name": project_name,
            "query": query,
        }
    )

    print(f"Metric: {metric_type} (last {window_minutes} minutes)")
    for time_series in results:
        for point in time_series.points:
            print(f"  {point.interval.end_time.isoformat()}: {point.value.double_value}")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and desired metric
    # Example: "your-project-id", "agent.googleapis.com/memory/used_bytes"
    PROJECT_ID = "your-project-id"  
    METRIC_TYPE = "agent.googleapis.com/memory/used_bytes"
    WINDOW_MINUTES = 5

    if PROJECT_ID == "your-project-id":
        print("Please replace 'your-project-id' with your actual Google Cloud Project ID.")
    else:
        query_metric_window(PROJECT_ID, METRIC_TYPE, WINDOW_MINUTES)
