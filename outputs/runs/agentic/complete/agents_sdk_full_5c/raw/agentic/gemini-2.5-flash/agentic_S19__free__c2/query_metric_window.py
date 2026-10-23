import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

# Google Cloud project ID
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

def query_metric_window(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int = 60,
):
    """Queries recent datapoints for a named metric over a time window."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    query_filter = f'metric.type = "{metric_type}"'

    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    time_series_data = []
    for ts in response.time_series:
        for point in ts.points:
            time_series_data.append(
                {
                    "metric": ts.metric.type,
                    "value": point.value.double_value or point.value.int64_value,
                    "timestamp": point.interval.end_time.timestamp(),
                }
            )
    return time_series_data

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID and metric type
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # metric_data = query_metric_window(
    #     PROJECT_ID,
    #     "compute.googleapis.com/instance/cpu/utilization",
    #     datetime.utcnow(),
    #     duration_minutes=10
    # )
    # for data_point in metric_data:
    #     print(data_point)
    pass
