import os
from datetime import datetime, timedelta, timezone
from google.cloud.monitoring_v3.types import (
    ListTimeSeriesRequest,
    TimeInterval,
    Aggregation,
)
from google.protobuf.duration_pb2 import Duration
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import GoogleCloudObservabilityClient

def get_aggregated_metric(
    gcp_project_id: str,
    metric_type: str,
    minutes_ago: int = 60,
) -> None:
    """
    Retrieves aggregated statistics for a metric over a time window.

    Args:
        gcp_project_id: The Google Cloud project ID.
        metric_type: The metric type to aggregate (e.g., "compute.googleapis.com/instance/disk/read_bytes_count").
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
    
    # Aggregate by summing up all the values over the window
    aggregation = Aggregation(
        alignment_period=Duration(seconds=minutes_ago * 60),
        per_series_aligner=Aggregation.Aligner.ALIGN_SUM,
        cross_series_reducer=Aggregation.Reducer.REDUCE_SUM,
        group_by_fields=["metric.labels.device_name"],
    )

    request = ListTimeSeriesRequest(
        name=client_helper.project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    results = client.list_time_series(request=request)
    print(f"Aggregated statistics for metric: {metric_type}")
    for result in results:
        device_name = result.metric.labels.get("device_name", "N/A")
        for point in result.points:
             print(f"- Device: {device_name}, Total: {point.value.int64_value}")

if __name__ == '__main__':
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable is not set.")
    
    # Example: Get total disk read bytes for GCE instances, summed across all instances
    get_aggregated_metric(
        gcp_project_id=project_id,
        metric_type="compute.googleapis.com/instance/disk/read_bytes_count"
    )
