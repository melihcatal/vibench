import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import google.api_core.exceptions


def aggregate_metric_stats(
    metric_name: str,
    project_id: str,
    start_time: datetime,
    end_time: datetime,
    aggregation_period_seconds: int = 300,
    aggregation_alignment: str = "ALIGN_MEAN",
    cross_series_reducer: str = "REDUCE_MEAN",
) -> Dict[str, Any]:
    """
    Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        project_id: Google Cloud project ID
        start_time: Start of time window
        end_time: End of time window
        aggregation_period_seconds: Alignment period in seconds
        aggregation_alignment: Per-series aligner (ALIGN_MEAN, ALIGN_MAX, ALIGN_MIN, ALIGN_SUM, etc.)
        cross_series_reducer: Cross-series reducer (REDUCE_MEAN, REDUCE_MAX, REDUCE_MIN, REDUCE_SUM, etc.)

    Returns:
        Dictionary containing aggregated statistics
    """
    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()
    interval.start_time = timestamp_pb2.Timestamp()
    interval.start_time.FromDatetime(start_time)
    interval.end_time = timestamp_pb2.Timestamp()
    interval.end_time.FromDatetime(end_time)

    filter_str = f'metric.type = "{metric_name}"'

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": aggregation_period_seconds}

    aligner_map = {
        "ALIGN_MEAN": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        "ALIGN_MAX": monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        "ALIGN_MIN": monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
        "ALIGN_SUM": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        "ALIGN_COUNT": monitoring_v3.Aggregation.Aligner.ALIGN_COUNT,
        "ALIGN_PERCENTILE_99": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_99,
        "ALIGN_PERCENTILE_95": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_95,
        "ALIGN_PERCENTILE_50": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_50,
    }

    reducer_map = {
        "REDUCE_MEAN": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        "REDUCE_MAX": monitoring_v3.Aggregation.Reducer.REDUCE_MAX,
        "REDUCE_MIN": monitoring_v3.Aggregation.Reducer.REDUCE_MIN,
        "REDUCE_SUM": monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
        "REDUCE_COUNT": monitoring_v3.Aggregation.Reducer.REDUCE_COUNT,
        "REDUCE_PERCENTILE_99": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_99,
        "REDUCE_PERCENTILE_95": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_95,
        "REDUCE_PERCENTILE_50": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_50,
        "REDUCE_STDDEV": monitoring_v3.Aggregation.Reducer.REDUCE_STDDEV,
    }

    aggregation.per_series_aligner = aligner_map.get(
        aggregation_alignment, monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    )
    aggregation.cross_series_reducer = reducer_map.get(
        cross_series_reducer, monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
    )

    try:
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.HEADERS,
                "aggregation": aggregation,
            }
        )

        aggregated_data = []
        total_points = 0
        min_value = float("inf")
        max_value = float("-inf")
        sum_values = 0.0

        for series in results:
            for point in series.points:
                if point.value.HasField("double_value"):
                    value = point.value.double_value
                    aggregated_data.append(
                        {
                            "timestamp": point.interval.end_time.ToDatetime(),
                            "value": value,
                            "metric_type": series.metric.type,
                            "resource_type": series.resource.type,
                        }
                    )

                    total_points += 1
                    min_value = min(min_value, value)
                    max_value = max(max_value, value)
                    sum_values += value

        stats = {
            "metric_name": metric_name,
            "time_window": {
                "start": start_time,
                "end": end_time,
            },
            "aggregation": {
                "alignment_period_seconds": aggregation_period_seconds,
                "per_series_aligner": aggregation_alignment,
                "cross_series_reducer": cross_series_reducer,
            },
            "statistics": {
                "total_points": total_points,
                "min": min_value if total_points > 0 else None,
                "max": max_value if total_points > 0 else None,
                "mean": sum_values / total_points if total_points > 0 else None,
                "sum": sum_values if total_points > 0 else None,
            },
            "series_count": len(results),
            "aggregated_points": aggregated_data,
        }

        return stats

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise
    except Exception as e:
        print(f"Error aggregating metric stats: {e}")
        raise
