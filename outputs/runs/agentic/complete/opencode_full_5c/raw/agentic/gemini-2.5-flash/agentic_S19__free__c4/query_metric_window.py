import os
import json
from observability_client import ObservabilityClient
from observability_models import (
    MetricQuery,
    TimeWindow,
    MetricTimeSeries,
    MetricDataPoint,
)
from typing import List


def query_metric_window(
    project_id: str, metric_type: str, start_time: str, end_time: str
) -> List[MetricTimeSeries]:
    """Queries recent datapoints for a named metric over a time window."""
    client = ObservabilityClient()
    time_window = TimeWindow(start_time=start_time, end_time=end_time)
    filter_string = f'metric.type = "{metric_type}"'
    query = MetricQuery(
        project_id=project_id,
        metric_type=metric_type,
        interval=time_window,
        filter_string=filter_string,
    )

    response = client.list_time_series(query)

    result_series = []
    for ts in response.time_series:
        points = []
        for point in ts.points:
            value = (
                point.int64_value
                if point.HasField("int66_value")
                else point.double_value
                if point.HasField("double_value")
                else point.string_value
                if point.HasField("string_value")
                else point.bool_value
                if point.HasField("bool_value")
                else 0
            )
            points.append(
                MetricDataPoint(
                    timestamp=str(point.interval.end_time.seconds),
                    value=value,
                    labels=dict(ts.resource.labels),
                )
            )

        result_series.append(
            MetricTimeSeries(
                metric_type=ts.metric.type,
                resource_labels=dict(ts.resource.labels),
                points=points,
            )
        )

    return result_series


if __name__ == "__main__":
    # Example usage (replace with your actual project ID, metric type, and time window)
    # Ensure GOOGLE_CLOUD_PROJECT environment variable is set or replace 'your-gcp-project-id' below
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    metric = "compute.googleapis.com/instance/cpu/utilization"
    # Unix timestamps
    end_time_ts = 1678886400  # Example: March 15, 2023 12:00:00 PM UTC
    start_time_ts = end_time_ts - 3600  # 1 hour before

    # For testing, ensure GOOGLE_CLOUD_PROJECT is set and you have monitoring data
    # For instance, create a simple VM in GCP to get 'compute.googleapis.com/instance/cpu/utilization' data

    try:
        metric_data = query_metric_window(
            project, metric, str(start_time_ts), str(end_time_ts)
        )
        print(json.dumps([m.__dict__ for m in metric_data], indent=2))
    except Exception as e:
        print(f"An error occurred: {e}")
        print(
            "Please ensure you have authenticated to GCP and have the necessary permissions."
        )
        print("You might need to set the GOOGLE_CLOUD_PROJECT environment variable.")
