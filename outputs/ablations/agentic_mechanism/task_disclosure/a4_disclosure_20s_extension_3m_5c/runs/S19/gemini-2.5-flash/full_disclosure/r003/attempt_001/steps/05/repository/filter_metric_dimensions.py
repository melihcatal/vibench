from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    resource_labels: dict = None,
    metric_labels: dict = None,
    minutes: int = 5
):
    """Queries metric data filtered by resource labels or dimensions.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        resource_labels: A dictionary of resource labels to filter by.
        metric_labels: A dictionary of metric labels to filter by.
        minutes: The number of minutes to query data for, ending now.

    Returns:
        A list of time series matching the filter.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.datetime.now(datetime.timezone.utc)
    end_time = Timestamp()
    end_time.FromDatetime(now)
    start_time = Timestamp()
    start_time.FromDatetime(now - datetime.timedelta(minutes=minutes))

    interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

    filter_str = f'metric.type = "{metric_type}"'

    if resource_labels:
        for key, value in resource_labels.items():
            filter_str += f' AND resource.labels.{key} = "{value}"'
    if metric_labels:
        for key, value in metric_labels.items():
            filter_str += f' AND metric.labels.{key} = "{value}"'

    # The aggregation needs to be specified for list_time_series
    # Here, we'll use a basic aggregation to get the latest value
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60 * 5},  # 5-minute alignment period
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_NONE,
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    return list(results)
