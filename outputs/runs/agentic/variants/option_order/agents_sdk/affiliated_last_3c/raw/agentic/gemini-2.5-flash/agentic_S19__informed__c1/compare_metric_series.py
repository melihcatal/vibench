from google.cloud import monitoring_v3
import os
import datetime

def _get_time_series_data(client, project_name, metric_type, interval, filter_str):
    """Helper to fetch time series data."""
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

def compare_metric_series(project_id: str, metric_type: str, end_time_str: str, duration_minutes: int, filter_a: dict, filter_b: dict):
    """Compares metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%SZ")
    start_time = end_time - datetime.timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat("T") + "Z",
        start_time=start_time.isoformat("T") + "Z",
    )

    # Construct filter strings for series A and B
    filter_parts_a = [f'metric.type = "{metric_type}"']
    for key, value in filter_a.items():
        filter_parts_a.append(f'{key} = "{value}"')
    filter_str_a = " AND ".join(filter_parts_a)

    filter_parts_b = [f'metric.type = "{metric_type}"']
    for key, value in filter_b.items():
        filter_parts_b.append(f'{key} = "{value}"')
    filter_str_b = " AND ".join(filter_parts_b)

    print(f"Fetching data for series A with filter: {filter_str_a}")
    data_series_a = _get_time_series_data(client, project_name, metric_type, interval, filter_str_a)
    print(f"Fetching data for series B with filter: {filter_str_b}")
    data_series_b = _get_time_series_data(client, project_name, metric_type, interval, filter_str_b)

    comparison_results = {
        "series_a": data_series_a,
        "series_b": data_series_b,
        "comparison_summary": f"Series A has {len(data_series_a)} data points, Series B has {len(data_series_b)} data points."
        # Further comparison logic can be added here, e.g., calculating differences, percentages, etc.
    }

    return comparison_results

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    metric_to_compare = "compute.googleapis.com/instance/cpu/utilization" # Example metric
    end_time_example = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    duration_example = 60 # minutes

    # Define filters for two different instances or zones
    filters_instance_1 = {"resource.type": "gce_instance", "resource.labels.instance_name": "instance-1"}
    filters_instance_2 = {"resource.type": "gce_instance", "resource.labels.instance_name": "instance-2"}
    # Adjust these filters to actual resources in your GCP project

    print(f"Comparing metric '{metric_to_compare}' for project '{project_id}' between {filters_instance_1} and {filters_instance_2}...")
    comparison = compare_metric_series(project_id, metric_to_compare, end_time_example, duration_example, filters_instance_1, filters_instance_2)
    print(comparison["comparison_summary"])
    # print(comparison) # Uncomment to see actual data
