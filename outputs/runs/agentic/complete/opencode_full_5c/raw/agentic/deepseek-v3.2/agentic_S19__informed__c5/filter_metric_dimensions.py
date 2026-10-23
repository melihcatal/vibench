from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import os
from datetime import datetime, timezone


def filter_metric_dimensions(
    metric_name, start_time, end_time, dimension_filters, project_id=None
):
    """
    Query metric data filtered by resource labels or dimensions.

    Args:
        metric_name: The metric type name
        start_time: Start time as datetime object
        end_time: End time as datetime object
        dimension_filters: Dictionary of dimension filters (e.g., {'resource.label.instance_id': 'instance-1'})
        project_id: Google Cloud project ID

    Returns:
        List of filtered metric time series
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

    filter_parts = [f'metric.type = "{metric_name}"']

    for key, value in dimension_filters.items():
        if key.startswith("resource.label."):
            filter_parts.append(f'{key} = "{value}"')
        elif key.startswith("metric.label."):
            filter_parts.append(f'{key} = "{value}"')
        else:
            filter_parts.append(f'{key} = "{value}"')

    filter_str = " AND ".join(filter_parts)

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

        filtered_series = []
        for series in results:
            series_data = {
                "metric_type": series.metric.type,
                "resource_type": series.resource.type,
                "metric_labels": dict(series.metric.labels),
                "resource_labels": dict(series.resource.labels),
                "points": [],
            }

            for point in series.points:
                series_data["points"].append(
                    {
                        "timestamp": point.interval.end_time.ToDatetime(),
                        "value": point.value.double_value
                        if point.value.HasField("double_value")
                        else point.value.int64_value,
                    }
                )

            filtered_series.append(series_data)

        return filtered_series

    except Exception as e:
        raise RuntimeError(f"Failed to filter metric dimensions: {str(e)}")
