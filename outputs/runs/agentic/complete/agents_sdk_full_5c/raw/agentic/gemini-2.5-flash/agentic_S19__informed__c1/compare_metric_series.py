
import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

def compare_metric_series(project_id: str, metric_type: str, filter_1: dict, filter_2: dict, minutes: int = 60):
    """
    Compares metric values for two resources or dimension filters over the same window
    using Google Cloud Monitoring. Returns data for both series.
    filter_1 and filter_2 examples: {"resource.labels.instance_name": "instance-1"}
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

    def _get_time_series_data(current_filter: dict):
        filter_parts = [f'metric.type = "{metric_type}"' ]
        for dim_key, dim_value in current_filter.items():
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

        series_data = []
        for ts in results:
            for point in ts.points:
                series_data.append({
                    "timestamp": point.interval.end_time,
                    "value": point.value.double_value or point.value.int64_value or point.value.bool_value or point.value.string_value,
                    "metric_labels": {k: v for k, v in ts.metric.labels.items()},
                    "resource_labels": {k: v for k, v in ts.resource.labels.items()},
                })
        return series_data

    series_1_data = _get_time_series_data(filter_1)
    series_2_data = _get_time_series_data(filter_2)

    return {"series_1": series_1_data, "series_2": series_2_data}

if __name__ == "__main__":
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    filter_1 = {"resource.labels.instance_name": "test-instance-1"}
    filter_2 = {"resource.labels.instance_name": "test-instance-2"}
    
    comparison_data = compare_metric_series(project_id, metric_type, filter_1, filter_2, minutes=10)
    
    print(f"Comparison of {metric_type} between {filter_1} and {filter_2}:")
    print(f"Series 1 ({filter_1}): {len(comparison_data['series_1'])} data points")
    for d in comparison_data['series_1'][:3]: # Print first 3 for brevity
        print(d)
    print(f"Series 2 ({filter_2}): {len(comparison_data['series_2'])} data points")
    for d in comparison_data['series_2'][:3]: # Print first 3 for brevity
        print(d)
