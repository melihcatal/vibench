from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import os
from datetime import datetime, timezone


def compare_metric_series(
    metric_name, start_time, end_time, filter_a, filter_b, project_id=None
):
    """
    Compare metric values for two resources or dimension filters over the same window.

    Args:
        metric_name: The metric type name
        start_time: Start time as datetime object
        end_time: End time as datetime object
        filter_a: Dictionary of dimension filters for series A
        filter_b: Dictionary of dimension filters for series B
        project_id: Google Cloud project ID

    Returns:
        Dictionary with comparison results
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

    def build_filter_string(base_filters):
        filter_parts = [f'metric.type = "{metric_name}"']
        for key, value in base_filters.items():
            filter_parts.append(f'{key} = "{value}"')
        return " AND ".join(filter_parts)

    filter_str_a = build_filter_string(filter_a)
    filter_str_b = build_filter_string(filter_b)

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 60}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN

    try:
        results_a = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str_a,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        results_b = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str_b,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        series_a_values = []
        series_b_values = []

        for series in results_a:
            for point in series.points:
                value = (
                    point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value
                )
                series_a_values.append(value)

        for series in results_b:
            for point in series.points:
                value = (
                    point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value
                )
                series_b_values.append(value)

        comparison = {
            "metric": metric_name,
            "window": {"start": start_time, "end": end_time},
            "series_a": {
                "filter": filter_a,
                "values": series_a_values,
                "count": len(series_a_values),
                "mean": sum(series_a_values) / len(series_a_values)
                if series_a_values
                else None,
                "max": max(series_a_values) if series_a_values else None,
                "min": min(series_a_values) if series_a_values else None,
            },
            "series_b": {
                "filter": filter_b,
                "values": series_b_values,
                "count": len(series_b_values),
                "mean": sum(series_b_values) / len(series_b_values)
                if series_b_values
                else None,
                "max": max(series_b_values) if series_b_values else None,
                "min": min(series_b_values) if series_b_values else None,
            },
        }

        if series_a_values and series_b_values:
            mean_a = sum(series_a_values) / len(series_a_values)
            mean_b = sum(series_b_values) / len(series_b_values)

            comparison["difference"] = {
                "mean_difference": mean_a - mean_b,
                "mean_percentage_diff": ((mean_a - mean_b) / mean_b * 100)
                if mean_b != 0
                else None,
                "a_vs_b_ratio": mean_a / mean_b if mean_b != 0 else None,
            }

        return comparison

    except Exception as e:
        raise RuntimeError(f"Failed to compare metric series: {str(e)}")
