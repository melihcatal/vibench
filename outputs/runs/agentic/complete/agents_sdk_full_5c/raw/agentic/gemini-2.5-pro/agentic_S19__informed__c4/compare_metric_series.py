import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any

from google.cloud.monitoring_v3.types import ListTimeSeriesRequest, TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import GoogleCloudObservabilityClient


def _get_series(
    client_helper: GoogleCloudObservabilityClient,
    metric_type: str,
    interval: TimeInterval,
    filter_dimension: Dict[str, str],
) -> List[Any]:
    """Helper to fetch a single time series."""
    key, value = list(filter_dimension.items())[0]
    filter_str = (
        f'metric.type = "{metric_type}" AND '
        f'resource.labels.{key} = "{value}"'
    )
    
    request = ListTimeSeriesRequest(
        name=client_helper.project_name,
        filter=filter_str,
        interval=interval,
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    
    results = client_helper.get_metric_service_client().list_time_series(request=request)
    return [
        (p.interval.end_time.ToDatetime(), p.value.double_value)
        for series in results
        for p in series.points
    ]


def compare_two_metric_series(
    gcp_project_id: str,
    metric_type: str,
    dimension_key: str,
    value1: str,
    value2: str,
    minutes_ago: int = 15,
) -> None:
    """
    Compares metric values for two resources over the same window.

    Args:
        gcp_project_id: The Google Cloud project ID.
        metric_type: The metric type to compare.
        dimension_key: The resource label key that distinguishes the two series.
        value1: The label value for the first resource.
        value2: The label value for the second resource.
        minutes_ago: The number of minutes for the comparison window.
    """
    try:
        client_helper = GoogleCloudObservabilityClient(project_id=gcp_project_id)
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

    print(f"Comparing '{metric_type}' for '{dimension_key}' between '{value1}' and '{value2}'")
    
    series1 = _get_series(client_helper, metric_type, interval, {dimension_key: value1})
    series2 = _get_series(client_helper, metric_type, interval, {dimension_key: value2})

    print(f"\n--- Data for {value1} ---")
    if series1:
        for ts, val in series1:
            print(f"  {ts}: {val:.4f}")
    else:
        print("No data found.")

    print(f"\n--- Data for {value2} ---")
    if series2:
        for ts, val in series2:
            print(f"  {ts}: {val:.4f}")
    else:
        print("No data found.")


if __name__ == '__main__':
    project_id = os.getenv("GCP_PROJECT_ID")
    instance1 = os.getenv("GCP_INSTANCE_1")
    instance2 = os.getenv("GCP_INSTANCE_2")

    if not all([project_id, instance1, instance2]):
        raise ValueError("GCP_PROJECT_ID, GCP_INSTANCE_1, and GCP_INSTANCE_2 must be set.")
        
    compare_two_metric_series(
        gcp_project_id=project_id,
        metric_type="compute.googleapis.com/instance/cpu/usage_time",
        dimension_key="instance_name",
        value1=instance1,
        value2=instance2
    )
