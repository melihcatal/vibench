import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import pytz


def compare_metric_series(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    filter_a: Dict[str, str],
    filter_b: Dict[str, str],
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        start_time: Start of the time window
        end_time: End of the time window
        filter_a: Dimension filters for first series
        filter_b: Dimension filters for second series
        project_id: Google Cloud project ID (defaults to GOOGLE_CLOUD_PROJECT env var)

    Returns:
        Comparison results with statistics for both series
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()
    interval.start_time = Timestamp()
    interval.start_time.FromDatetime(start_time)
    interval.end_time = Timestamp()
    interval.end_time.FromDatetime(end_time)

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 60}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN

    def get_series_values(
        filters: Dict[str, str],
    ) -> Tuple[List[float], Dict[str, Any]]:
        filter_parts = [f'metric.type = "{metric_name}"']
        for dim_name, dim_value in filters.items():
            filter_parts.append(f'resource.labels.{dim_name} = "{dim_value}"')

        filter_str = " AND ".join(filter_parts)

        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            aggregation=aggregation,
        )

        values = []
        series_info = {}

        for time_series in client.list_time_series(request):
            if not series_info:
                series_info = {
                    "resource_labels": dict(time_series.resource.labels),
                    "resource_type": time_series.resource.type,
                }

            for point in time_series.points:
                point_value = point.value.double_value or point.value.int64_value
                if point_value is not None:
                    values.append(float(point_value))

        return values, series_info

    values_a, info_a = get_series_values(filter_a)
    values_b, info_b = get_series_values(filter_b)

    def calculate_stats(values: List[float]) -> Dict[str, Any]:
        if not values:
            return {"count": 0, "mean": None, "min": None, "max": None, "p95": None}

        sorted_vals = sorted(values)
        n = len(sorted_vals)

        return {
            "count": n,
            "mean": sum(values) / n,
            "min": min(values),
            "max": max(values),
            "p95": sorted_vals[int(0.95 * n) - 1] if n >= 20 else None,
        }

    stats_a = calculate_stats(values_a)
    stats_b = calculate_stats(values_b)

    comparison = {}
    if stats_a["mean"] is not None and stats_b["mean"] is not None:
        mean_diff = stats_a["mean"] - stats_b["mean"]
        mean_diff_pct = (
            (mean_diff / stats_b["mean"]) * 100
            if stats_b["mean"] != 0
            else float("inf")
        )

        comparison = {
            "mean_difference": mean_diff,
            "mean_difference_percent": mean_diff_pct,
            "a_higher": mean_diff > 0,
            "significant_difference": abs(mean_diff_pct) > 10.0,
        }

    return {
        "metric_name": metric_name,
        "time_window": {"start": start_time.isoformat(), "end": end_time.isoformat()},
        "series_a": {"filters": filter_a, "info": info_a, "statistics": stats_a},
        "series_b": {"filters": filter_b, "info": info_b, "statistics": stats_b},
        "comparison": comparison,
    }


if __name__ == "__main__":
    end_time = datetime.now(pytz.UTC)
    start_time = end_time - timedelta(hours=2)

    comparison_result = compare_metric_series(
        metric_name="compute.googleapis.com/instance/cpu/utilization",
        start_time=start_time,
        end_time=end_time,
        filter_a={"instance_id": "instance-1", "zone": "us-central1-a"},
        filter_b={"instance_id": "instance-2", "zone": "us-central1-b"},
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )

    print(f"Comparison result: {comparison_result}")
