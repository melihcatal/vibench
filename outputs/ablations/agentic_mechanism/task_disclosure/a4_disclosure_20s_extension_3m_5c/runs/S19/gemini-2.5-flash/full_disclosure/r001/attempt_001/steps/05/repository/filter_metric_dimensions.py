from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import types
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    resource_type: str,
    resource_labels: dict,
    end_time: datetime.datetime,
    minutes_ago: int = 60,
):
    """
    Queries metric data filtered by resource labels or dimensions.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        resource_type: The type of monitored resource (e.g., "gce_instance").
        resource_labels: A dictionary of resource labels to filter by (e.g., {"instance_id": "12345"}).
        end_time: The end time for the metric data.
        minutes_ago: The number of minutes before `end_time` to query. Defaults to 60.

    Returns:
        A list of TimeSeries objects containing the queried metric data.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - datetime.timedelta(minutes=minutes_ago)

    # Convert datetime objects to Timestamp protobuf objects
    interval = types.TimeInterval()
    interval.end_time.seconds = int(end_time.timestamp())
    interval.start_time.seconds = int(start_time.timestamp())

    # Build the filter string for resource labels
    resource_filter_parts = [
        f'resource.type = "{resource_type}"'
    ]
    for key, value in resource_labels.items():
        resource_filter_parts.append(f'resource.labels.{key} = "{value}"')
    resource_filter = " AND ".join(resource_filter_parts)

    filter_string = f'metric.type = "{metric_type}" AND {resource_filter}'

    request = types.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_string,
        interval=interval,
        view=types.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    response = client.list_time_series(request=request)
    return list(response)
