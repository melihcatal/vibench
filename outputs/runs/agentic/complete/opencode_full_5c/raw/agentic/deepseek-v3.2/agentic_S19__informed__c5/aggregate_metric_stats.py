from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import os
from datetime import datetime, timezone


def aggregate_metric_stats(
    metric_name, start_time, end_time, project_id=None, aggregation_type="mean"
):
    """
    Retrieve aggregated statistics for a metric over a time window.

    Args:
        metric_name: The metric type name
        start_time: Start time as datetime object
        end_time: End time as datetime object
        project_id: Google Cloud project ID
        aggregation_type: Type of aggregation ('mean', 'max', 'min', 'sum', 'count', 'percentile')

    Returns:
        Dictionary with aggregated statistics
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
    aggregation.alignment_period = {"seconds": 300}

    aligner_map = {
        "mean": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        "max": monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        "min": monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
        "sum": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        "count": monitoring_v3.Aggregation.Aligner.ALIGN_COUNT,
        "percentile_50": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_50,
        "percentile_95": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_95,
        "percentile_99": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_99,
    }

    if aggregation_type not in aligner_map:
        raise ValueError(f"Unsupported aggregation type: {aggregation_type}")

    aggregation.per_series_aligner = aligner_map[aggregation_type]

    cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN

    try:
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
                "secondary_aggregation": monitoring_v3.Aggregation(
                    alignment_period={"seconds": 300},
                    cross_series_reducer=cross_series_reducer,
                ),
            }
        )

        aggregated_values = []
        for series in results:
            for point in series.points:
                value = (
                    point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value
                )
                aggregated_values.append(value)

        if not aggregated_values:
            return {
                "metric": metric_name,
                "aggregation_type": aggregation_type,
                "start_time": start_time,
                "end_time": end_time,
                "value": None,
                "count": 0,
            }

        stats = {
            "metric": metric_name,
            "aggregation_type": aggregation_type,
            "start_time": start_time,
            "end_time": end_time,
            "value": aggregated_values[-1] if aggregated_values else None,
            "count": len(aggregated_values),
            "all_values": aggregated_values,
        }

        if aggregation_type == "mean" and aggregated_values:
            stats["mean"] = sum(aggregated_values) / len(aggregated_values)
        elif aggregation_type == "max" and aggregated_values:
            stats["max"] = max(aggregated_values)
        elif aggregation_type == "min" and aggregated_values:
            stats["min"] = min(aggregated_values)
        elif aggregation_type == "sum" and aggregated_values:
            stats["sum"] = sum(aggregated_values)

        return stats

    except Exception as e:
        raise RuntimeError(f"Failed to aggregate metric stats: {str(e)}")
