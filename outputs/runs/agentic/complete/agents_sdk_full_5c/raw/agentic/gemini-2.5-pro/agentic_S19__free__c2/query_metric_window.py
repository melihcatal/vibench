import os
import time
from typing import List
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import ClientFactory
from observability_models import MetricData, TimeSeriesPoint


def query_gcp_metric_window(
    project_id: str,
    metric_filter: str,
    minutes_ago: int = 60,
) -> List[MetricData]:
    """
    Queries recent datapoints for a named metric over a time window from GCP Monitoring.

    Args:
        project_id: The GCP project ID.
        metric_filter: The filter string for the metric.
                       e.g., 'metric.type = "compute.googleapis.com/instance/cpu/utilization"'
        minutes_ago: The number of minutes in the past to query.

    Returns:
        A list of MetricData objects.
    """
    client = ClientFactory.get_google_monitoring_client()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": Timestamp(seconds=seconds, nanos=nanos),
            "start_time": Timestamp(seconds=(seconds - minutes_ago * 60), nanos=nanos),
        }
    )

    request = {
        "name": project_name,
        "filter": metric_filter,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results = client.list_time_series(request)
    output = []

    for result in results:
        points = [
            TimeSeriesPoint(timestamp=p.interval.start_time.timestamp(), value=p.value.double_value)
            for p in result.points
        ]
        metric_data = MetricData(
            metric_name=result.metric.type,
            points=points,
            dimensions=dict(result.metric.labels),
        )
        output.append(metric_data)

    return output

# Example usage would require authentication and a running GCP project.
# if __name__ == '__main__':
#     gcp_project_id = os.environ.get("GCP_PROJECT_ID")
#     if gcp_project_id:
#         cpu_utilization_filter = 'metric.type = "compute.googleapis.com/instance/cpu/utilization"'
#         data = query_gcp_metric_window(gcp_project_id, cpu_utilization_filter, minutes_ago=30)
#         for series in data:
#             print(f"Metric: {series.metric_name}, Dimensions: {series.dimensions}")
#             for point in series.points:
#                 print(f"  - Time: {point.timestamp}, Value: {point.value}")
#     else:
#         print("GCP_PROJECT_ID environment variable not set.")
