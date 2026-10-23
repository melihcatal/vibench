import os
from datetime import datetime, timedelta, timezone

from google.cloud.monitoring_v3.services.metric_service import MetricServiceClient
from google.cloud.monitoring_v3.types import ListTimeSeriesRequest, TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import GoogleCloudObservabilityClient

def query_metric_window(
    gcp_project_id: str,
    metric_type: str,
    minutes_ago: int = 60,
) -> None:
    """
    Queries recent datapoints for a named metric over a time window.

    Args:
        gcp_project_id: The Google Cloud project ID.
        metric_type: The metric type to query (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        minutes_ago: The number of minutes in the past to start the query window.
    """
    try:
        client_helper = GoogleCloudObservabilityClient(project_id=gcp_project_id)
        client = client_helper.get_metric_service_client()
    except Exception as e:
        print(f"Failed to create observability client: {e}")
        return

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)

    start_timestamp = Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = Timestamp()
    end_timestamp.FromDatetime(now)

    interval = TimeInterval(
        start_time=start_timestamp,
        end_time=end_timestamp,
    )

    request = ListTimeSeriesRequest(
        name=client_helper.project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = client.list_time_series(request=request)
    print(f"Querying data for metric: {metric_type}")
    for result in results:
        print(f"- Resource: {result.resource.labels}")
        for point in result.points:
            print(f"  - Timestamp: {point.interval.end_time.ToDatetime()}, Value: {point.value.double_value}")

if __name__ == '__main__':
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable is not set.")
    
    # Example: Query CPU usage for GCE instances
    query_metric_window(
        gcp_project_id=project_id,
        metric_type="compute.googleapis.com/instance/cpu/usage_time"
    )
