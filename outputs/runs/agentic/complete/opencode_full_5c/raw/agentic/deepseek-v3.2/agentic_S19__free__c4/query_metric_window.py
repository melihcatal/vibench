import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import google.api_core.exceptions


def query_metric_window(
    metric_name: str,
    project_id: str,
    start_time: datetime,
    end_time: datetime,
    filter_labels: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Query recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        project_id: Google Cloud project ID
        start_time: Start of time window
        end_time: End of time window
        filter_labels: Optional resource labels to filter by

    Returns:
        List of metric datapoints with timestamps and values
    """
    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()
    interval.start_time = timestamp_pb2.Timestamp()
    interval.start_time.FromDatetime(start_time)
    interval.end_time = timestamp_pb2.Timestamp()
    interval.end_time.FromDatetime(end_time)

    filter_str = f'metric.type = "{metric_name}"'
    if filter_labels:
        label_filters = []
        for key, value in filter_labels.items():
            label_filters.append(f'resource.labels.{key} = "{value}"')
        if label_filters:
            filter_str += f" AND {' AND '.join(label_filters)}"

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 60}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_NONE

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
                datapoint = {
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else None,
                    "metric_type": series.metric.type,
                    "resource_type": series.resource.type,
                    "resource_labels": dict(series.resource.labels),
                    "metric_labels": dict(series.metric.labels),
                }
                datapoints.append(datapoint)

        return datapoints

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise
    except Exception as e:
        print(f"Error querying metric window: {e}")
        raise
