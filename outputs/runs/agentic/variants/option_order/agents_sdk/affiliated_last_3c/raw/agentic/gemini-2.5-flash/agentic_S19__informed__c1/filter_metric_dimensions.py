from google.cloud import monitoring_v3
import os
import datetime

def filter_metric_dimensions(project_id: str, metric_type: str, end_time_str: str, duration_minutes: int, filters: dict):
    """Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%SZ")
    start_time = end_time - datetime.timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat("T") + "Z",
        start_time=start_time.isoformat("T") + "Z",
    )

    # Base filter for metric type
    filter_parts = [f'metric.type = "{metric_type}"']

    # Add dimension filters
    # Filters should be in the format like: 'resource.label."instance_id" = "your-instance-id"' or 'metric.label."state" = "running"'
    for key, value in filters.items():
        filter_parts.append(f'{key} = "{value}"')

    filter_str = " AND ".join(filter_parts)

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    filtered_data = []
    for series in results:
        for point in series.points:
            filtered_data.append({
                "value": point.value.double_value or point.value.int64_value or point.value.string_value or str(point.value.bool_value),
                "timestamp": point.interval.end_time.isoformat(),
                "metric_labels": dict(series.metric.labels),
                "resource_labels": dict(series.resource.labels),
            })
    return filtered_data

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    metric_to_filter = "agent.googleapis.com/memory/used_bytes" # Example metric
    end_time_example = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    duration_example = 30 # minutes
    # Example filters: 'resource.type': 'gce_instance', 'resource.labels.instance_id': '1234567890'
    dimension_filters = {
        "resource.type": "gce_instance",
        "resource.labels.zone": "us-central1-a" # Example, replace with actual zone or instance_id
    }

    print(f"Filtering metric '{metric_to_filter}' for project '{project_id}' with filters {dimension_filters}...")
    data = filter_metric_dimensions(project_id, metric_to_filter, end_time_example, duration_example, dimension_filters)
    print(f"Retrieved {len(data)} filtered data points.")
    # print(data) # Uncomment to see actual data
