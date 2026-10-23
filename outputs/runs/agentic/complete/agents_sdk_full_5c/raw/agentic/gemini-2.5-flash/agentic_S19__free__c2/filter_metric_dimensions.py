import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

# Google Cloud project ID
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int = 60,
    dimension_filters: dict = None,
):
    """Queries metric data filtered by resource labels or dimensions."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    query_filter = f'metric.type = "{metric_type}"'

    if dimension_filters:
        for key, value in dimension_filters.items():
            query_filter += f' AND resource.labels.{key} = "{value}"'

    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    filtered_data = []
    for ts in response.time_series:
        for point in ts.points:
            filtered_data.append(
                {
                    "metric": ts.metric.type,
                    "resource_labels": dict(ts.resource.labels),
                    "value": point.value.double_value or point.value.int64_value,
                    "timestamp": point.interval.end_time.timestamp(),
                }
            )
    return filtered_data

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID and metric type
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # filtered_metrics = filter_metric_dimensions(
    #     PROJECT_ID,
    #     "compute.googleapis.com/instance/cpu/utilization",
    #     datetime.utcnow(),
    #     duration_minutes=10,
    #     dimension_filters={"instance_name": "my-instance"}
    # )
    # for metric in filtered_metrics:
    #     print(metric)
    pass
