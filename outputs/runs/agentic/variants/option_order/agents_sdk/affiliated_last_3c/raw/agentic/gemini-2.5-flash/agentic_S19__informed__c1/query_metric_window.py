from google.cloud import monitoring_v3
import os
import datetime

def query_metric_window(project_id: str, metric_type: str, end_time_str: str, duration_minutes: int):
    """Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%SZ")
    start_time = end_time - datetime.timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat("T") + "Z",
        start_time=start_time.isoformat("T") + "Z",
    )

    # Example filter: "metric.type = \"logging.googleapis.com/log_entry_count\""
    # Replace with the actual metric type you want to query
    filter_str = f'metric.type = "{metric_type}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    data_points = []
    for series in results:
        for point in series.points:
            data_points.append({
                "value": point.value.double_value or point.value.int64_value or point.value.string_value or str(point.value.bool_value),
                "timestamp": point.interval.end_time.isoformat(),
                "metric_labels": dict(series.metric.labels),
                "resource_labels": dict(series.resource.labels),
            })
    return data_points

if __name__ == "__main__":
    # This assumes GOOGLE_APPLICATION_CREDENTIALS is set up
    # Replace with your actual project ID and metric type
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    metric_to_query = "logging.googleapis.com/log_entry_count" # Example metric
    end_time_example = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    duration_example = 60 # minutes

    print(f"Querying metric '{metric_to_query}' for project '{project_id}'...")
    data = query_metric_window(project_id, metric_to_query, end_time_example, duration_example)
    print(f"Retrieved {len(data)} data points.")
    # print(data) # Uncomment to see actual data
