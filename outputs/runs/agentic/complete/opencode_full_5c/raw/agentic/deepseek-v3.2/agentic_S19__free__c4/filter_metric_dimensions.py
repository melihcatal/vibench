import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import google.api_core.exceptions


def filter_metric_dimensions(
    metric_name: str,
    project_id: str,
    start_time: datetime,
    end_time: datetime,
    dimension_filters: Dict[str, str],
    metric_label_filters: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Query metric data filtered by resource labels or dimensions using Google Cloud Monitoring.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        project_id: Google Cloud project ID
        start_time: Start of time window
        end_time: End of time window
        dimension_filters: Resource label filters (e.g., {'instance_id': 'instance-1', 'zone': 'us-central1-a'})
        metric_label_filters: Optional metric label filters

    Returns:
        List of filtered metric datapoints
    """
    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()
    interval.start_time = timestamp_pb2.Timestamp()
    interval.start_time.FromDatetime(start_time)
    interval.end_time = timestamp_pb2.Timestamp()
    interval.end_time.FromDatetime(end_time)

    filter_parts = [f'metric.type = "{metric_name}"']

    for dim_key, dim_value in dimension_filters.items():
        filter_parts.append(f'resource.labels.{dim_key} = "{dim_value}"')

    if metric_label_filters:
        for label_key, label_value in metric_label_filters.items():
            filter_parts.append(f'metric.labels.{label_key} = "{label_value}"')

    filter_str = " AND ".join(filter_parts)

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

        filtered_data = []
        for series in results:
            series_info = {
                "metric_type": series.metric.type,
                "resource_type": series.resource.type,
                "resource_labels": dict(series.resource.labels),
                "metric_labels": dict(series.metric.labels),
                "points": [],
            }

            for point in series.points:
                point_data = {
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else None,
                }
                series_info["points"].append(point_data)

            filtered_data.append(series_info)

        return filtered_data

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise
    except Exception as e:
        print(f"Error filtering metric dimensions: {e}")
        raise


def get_available_dimensions(
    metric_name: str, project_id: str, lookback_hours: int = 24
) -> Dict[str, List[str]]:
    """
    Get available dimension values for a metric.

    Args:
        metric_name: The metric type name
        project_id: Google Cloud project ID
        lookback_hours: Hours to look back for dimension values

    Returns:
        Dictionary mapping dimension names to available values
    """
    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=lookback_hours)

    interval = monitoring_v3.TimeInterval()
    interval.start_time = timestamp_pb2.Timestamp()
    interval.start_time.FromDatetime(start_time)
    interval.end_time = timestamp_pb2.Timestamp()
    interval.end_time.FromDatetime(end_time)

    filter_str = f'metric.type = "{metric_name}"'

    try:
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.HEADERS,
            }
        )

        dimension_values = {}

        for series in results:
            for label_key, label_value in series.resource.labels.items():
                if label_key not in dimension_values:
                    dimension_values[label_key] = set()
                dimension_values[label_key].add(label_value)

            for label_key, label_value in series.metric.labels.items():
                dimension_key = f"metric.{label_key}"
                if dimension_key not in dimension_values:
                    dimension_values[dimension_key] = set()
                dimension_values[dimension_key].add(label_value)

        return {k: list(v) for k, v in dimension_values.items()}

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise
    except Exception as e:
        print(f"Error getting available dimensions: {e}")
        raise
