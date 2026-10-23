
import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

def query_metric_window(project_id: str, metric_type: str, minutes: int = 60):
    """
    Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    start_time = (now - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(now.timestamp())},
        start_time={"seconds": int((now - timedelta(minutes=minutes)).timestamp())},
    )

    # Example filter for a generic metric
    # For more complex filters, refer to Google Cloud Monitoring documentation
    # https://cloud.google.com/monitoring/api/v3/filters
    filter_str = f'metric.type = "{metric_type}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    time_series_data = []
    for ts in results:
        for point in ts.points:
            time_series_data.append({
                "metric_kind": ts.metric_kind.name,
                "value_type": ts.value_type.name,
                "timestamp": point.interval.end_time,
                "value": point.value.double_value or point.value.int64_value or point.value.bool_value or point.value.string_value,
                "metric_labels": {k: v for k, v in ts.metric.labels.items()},
                "resource_labels": {k: v for k, v in ts.resource.labels.items()},
            })
    return time_series_data

if __name__ == "__main__":
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    # Replace 'your-gcp-project-id' and 'compute.googleapis.com/instance/cpu/utilization' with actual values.
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    data = query_metric_window(project_id, metric_type, minutes=10)
    print(f"Retrieved {len(data)} data points for {metric_type}:")
    for d in data[:5]: # Print first 5 for brevity
        print(d)
