import os
from datetime import datetime, timedelta, timezone

from google.cloud.monitoring_v3.types import ListTimeSeriesRequest, TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import GoogleCloudObservabilityClient

def query_metric_with_dimension_filter(
    gcp_project_id: str,
    metric_type: str,
    dimension_key: str,
    dimension_value: str,
    minutes_ago: int = 30,
) -> None:
    """
    Queries metric data filtered by a specific resource label or dimension.

    Args:
        gcp_project_id: The Google Cloud project ID.
        metric_type: The metric type to query.
        dimension_key: The resource label key to filter on (e.g., "instance_name").
        dimension_value: The specific value for the dimension key.
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
    
    # Construct a filter that includes the resource dimension
    filter_str = (
        f'metric.type = "{metric_type}" AND '
        f'resource.labels.{dimension_key} = "{dimension_value}"'
    )
    
    request = ListTimeSeriesRequest(
        name=client_helper.project_name,
        filter=filter_str,
        interval=interval,
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = client.list_time_series(request=request)
    print(f"Querying data for metric '{metric_type}' with filter '{dimension_key}=\"{dimension_value}\"':")

    for result in results:
        print(f"Data for {result.resource.labels}:")
        for point in result.points:
            print(f"  - Time: {point.interval.end_time.ToDatetime()}, Value: {point.value.double_value}")

if __name__ == '__main__':
    project_id = os.getenv("GCP_PROJECT_ID")
    target_instance_name = os.getenv("GCP_TARGET_INSTANCE_NAME")

    if not project_id or not target_instance_name:
        raise ValueError("GCP_PROJECT_ID and GCP_TARGET_INSTANCE_NAME environment variables must be set.")
    
    # Example: Query CPU usage for a specific GCE instance
    query_metric_with_dimension_filter(
        gcp_project_id=project_id,
        metric_type="compute.googleapis.com/instance/cpu/usage_time",
        dimension_key="instance_name",
        dimension_value=target_instance_name
    )
