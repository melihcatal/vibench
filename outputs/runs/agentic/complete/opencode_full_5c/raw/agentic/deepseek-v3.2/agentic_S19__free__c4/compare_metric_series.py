import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import google.api_core.exceptions


def compare_metric_series(
    metric_name: str,
    project_id: str,
    start_time: datetime,
    end_time: datetime,
    series_a_filters: Dict[str, str],
    series_b_filters: Dict[str, str],
    aggregation_period_seconds: int = 300,
) -> Dict[str, Any]:
    """
    Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        project_id: Google Cloud project ID
        start_time: Start of time window
        end_time: End of time window
        series_a_filters: Filters for first series (resource labels or metric labels)
        series_b_filters: Filters for second series (resource labels or metric labels)
        aggregation_period_seconds: Alignment period in seconds

    Returns:
        Dictionary containing comparison results
    """
    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()
    interval.start_time = timestamp_pb2.Timestamp()
    interval.start_time.FromDatetime(start_time)
    interval.end_time = timestamp_pb2.Timestamp()
    interval.end_time.FromDatetime(end_time)

    def build_filter_string(filters: Dict[str, str]) -> str:
        filter_parts = [f'metric.type = "{metric_name}"']
        for key, value in filters.items():
            if key.startswith("metric."):
                label_key = key.replace("metric.", "")
                filter_parts.append(f'metric.labels.{label_key} = "{value}"')
            else:
                filter_parts.append(f'resource.labels.{key} = "{value}"')
        return " AND ".join(filter_parts)

    filter_a = build_filter_string(series_a_filters)
    filter_b = build_filter_string(series_b_filters)

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": aggregation_period_seconds}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN

    try:
        series_a_results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_a,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        series_b_results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_b,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        def extract_series_data(
            series_results, series_label: str
        ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
            points = []
            values = []

            for series in series_results:
                for point in series.points:
                    if point.value.HasField("double_value"):
                        point_data = {
                            "timestamp": point.interval.end_time.ToDatetime(),
                            "value": point.value.double_value,
                            "series_label": series_label,
                            "resource_labels": dict(series.resource.labels),
                            "metric_labels": dict(series.metric.labels),
                        }
                        points.append(point_data)
                        values.append(point.value.double_value)

            stats = {}
            if values:
                stats = {
                    "mean": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                    "sum": sum(values),
                }

            return points, stats

        series_a_points, series_a_stats = extract_series_data(
            series_a_results, "Series A"
        )
        series_b_points, series_b_stats = extract_series_data(
            series_b_results, "Series B"
        )

        comparison_stats = {}
        if series_a_stats and series_b_stats:
            mean_diff = series_a_stats["mean"] - series_b_stats["mean"]
            mean_diff_percent = (
                (mean_diff / series_b_stats["mean"]) * 100
                if series_b_stats["mean"] != 0
                else float("inf")
            )

            comparison_stats = {
                "mean_difference": mean_diff,
                "mean_difference_percent": mean_diff_percent,
                "ratio": series_a_stats["mean"] / series_b_stats["mean"]
                if series_b_stats["mean"] != 0
                else float("inf"),
                "a_mean_vs_b_mean": f"{series_a_stats['mean']:.3f} vs {series_b_stats['mean']:.3f}",
                "a_min_vs_b_min": f"{series_a_stats['min']:.3f} vs {series_b_stats['min']:.3f}",
                "a_max_vs_b_max": f"{series_a_stats['max']:.3f} vs {series_b_stats['max']:.3f}",
            }

        aligned_points = []
        a_points_by_time = {p["timestamp"]: p["value"] for p in series_a_points}
        b_points_by_time = {p["timestamp"]: p["value"] for p in series_b_points}

        all_timestamps = sorted(
            set(list(a_points_by_time.keys()) + list(b_points_by_time.keys()))
        )

        for timestamp in all_timestamps:
            aligned_point = {
                "timestamp": timestamp,
                "series_a_value": a_points_by_time.get(timestamp),
                "series_b_value": b_points_by_time.get(timestamp),
                "difference": None,
                "difference_percent": None,
            }

            if (
                aligned_point["series_a_value"] is not None
                and aligned_point["series_b_value"] is not None
            ):
                aligned_point["difference"] = (
                    aligned_point["series_a_value"] - aligned_point["series_b_value"]
                )
                if aligned_point["series_b_value"] != 0:
                    aligned_point["difference_percent"] = (
                        aligned_point["difference"] / aligned_point["series_b_value"]
                    ) * 100

            aligned_points.append(aligned_point)

        result = {
            "metric_name": metric_name,
            "time_window": {
                "start": start_time,
                "end": end_time,
            },
            "series_a": {
                "filters": series_a_filters,
                "filter_string": filter_a,
                "stats": series_a_stats,
                "point_count": len(series_a_points),
            },
            "series_b": {
                "filters": series_b_filters,
                "filter_string": filter_b,
                "stats": series_b_stats,
                "point_count": len(series_b_points),
            },
            "comparison": comparison_stats,
            "aligned_points": aligned_points,
            "total_aligned_points": len(aligned_points),
        }

        return result

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise
    except Exception as e:
        print(f"Error comparing metric series: {e}")
        raise
