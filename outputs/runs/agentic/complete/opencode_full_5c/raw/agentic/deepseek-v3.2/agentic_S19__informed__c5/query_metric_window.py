from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import os
from datetime import datetime, timezone


def query_metric_window(metric_name, start_time, end_time, project_id=None):
    """
    Query recent datapoints for a named metric over a time window.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        start_time: Start time as datetime object
        end_time: End time as datetime object
        project_id: Google Cloud project ID (defaults to GOOGLE_CLOUD_PROJECT env var)

    Returns:
        List of metric time series data points
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()

    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)
    interval.start_time = start_timestamp

    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(end_time)
    interval.end_time = end_timestamp

    filter_str = f'metric.type = "{metric_name}"'

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 60}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN

    try:
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        datapoints = []
        for series in results:
            for point in series.points:
                datapoints.append(
                    {
                        "metric_type": series.metric.type,
                        "resource_type": series.resource.type,
                        "timestamp": point.interval.end_time.ToDatetime(),
                        "value": point.value.double_value
                        if point.value.HasField("double_value")
                        else point.value.int64_value,
                        "labels": dict(series.metric.labels),
                    }
                )

        return datapoints

    except Exception as e:
        raise RuntimeError(f"Failed to query metric window: {str(e)}")
