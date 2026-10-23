
import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id: str, metric_type: str, filter_dimensions: dict, minutes: int = 60):
    """
    Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring.
    filter_dimensions example: {"resource.labels.instance_name": "my-instance"}
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

    # Base filter for the metric type
    filter_parts = [f'metric.type = "{metric_type}"' ]

    # Add dimension filters
    for dim_key, dim_value in filter_dimensions.items():
        filter_parts.append(f'{dim_key} = "{dim_value}"')

    full_filter_str = " AND ".join(filter_parts)

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": full_filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    filtered_data = []
    for ts in results:
        for point in ts.points:
            filtered_data.append({
                "timestamp": point.interval.end_time,
                "value": point.value.double_value or point.value.int64_value or point.value.bool_value or point.value.string_value,
                "metric_labels": {k: v for k, v in ts.metric.labels.items()},
                "resource_labels": {k: v for k, v in ts.resource.labels.items()},
            })
    return filtered_data

if __name__ == "__main__":
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    # Example: filter by a specific instance name
    dimensions = {"resource.labels.instance_name": "test-instance-1"}
    data = filter_metric_dimensions(project_id, metric_type, dimensions, minutes=10)
    print(f"Retrieved {len(data)} filtered data points for {metric_type} with dimensions {dimensions}:")
    for d in data[:5]:
        print(d)
