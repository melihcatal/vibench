import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def compare_metric_series(metric_name, filter_a, filter_b, window_minutes=60):
    """
    Compare metric values for two resources or dimension filters over the same window.

    Args:
        metric_name: The name of the metric to query
        filter_a: Dictionary of dimension filters for series A
        filter_b: Dictionary of dimension filters for series B
        window_minutes: Time window in minutes to query (default: 60)

    Returns:
        Dictionary with comparison results including series data and statistics
    """
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = timestamp_pb2.Timestamp(seconds=int(now.timestamp()))
    interval.start_time = timestamp_pb2.Timestamp(seconds=int(start_time.timestamp()))

    def build_filter_string(filters):
        filter_parts = [f'metric.type = "{metric_name}"']
        for key, value in filters.items():
            if key.startswith("resource.labels."):
                filter_parts.append(f'{key} = "{value}"')
            elif key.startswith("metric.labels."):
                filter_parts.append(f'{key} = "{value}"')
            else:
                filter_parts.append(f'{key} = "{value}"')
        return " AND ".join(filter_parts)

    filter_a_str = build_filter_string(filter_a)
    filter_b_str = build_filter_string(filter_b)

    def query_series(filter_str):
        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        series_data = []
        for time_series in client.list_time_series(request):
            for point in time_series.points:
                if point.value.HasField("double_value"):
                    series_data.append(
                        {
                            "timestamp": point.interval.end_time.ToDatetime(),
                            "value": point.value.double_value,
                            "resource_labels": dict(time_series.resource.labels),
                            "metric_labels": dict(time_series.metric.labels),
                        }
                    )
        return series_data

    series_a = query_series(filter_a_str)
    series_b = query_series(filter_b_str)

    def calculate_stats(series):
        if not series:
            return {"count": 0, "mean": None, "min": None, "max": None}

        values = [point["value"] for point in series]
        return {
            "count": len(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }

    stats_a = calculate_stats(series_a)
    stats_b = calculate_stats(series_b)

    comparison = {
        "series_a": {"data": series_a, "stats": stats_a, "filter": filter_a},
        "series_b": {"data": series_b, "stats": stats_b, "filter": filter_b},
        "comparison": {
            "mean_difference": (stats_a["mean"] - stats_b["mean"])
            if stats_a["mean"] and stats_b["mean"]
            else None,
            "relative_difference": (
                (stats_a["mean"] - stats_b["mean"]) / stats_b["mean"] * 100
            )
            if stats_a["mean"] and stats_b["mean"] and stats_b["mean"] != 0
            else None,
            "window_minutes": window_minutes,
            "metric": metric_name,
        },
    }

    return comparison


if __name__ == "__main__":
    sample_metric = "compute.googleapis.com/instance/cpu/utilization"
    filter_a = {"resource.labels.instance_id": "instance-12345"}
    filter_b = {"resource.labels.instance_id": "instance-67890"}

    try:
        comparison = compare_metric_series(
            sample_metric, filter_a, filter_b, window_minutes=30
        )
        print(f"Comparison results:")
        print(f"  Series A count: {comparison['series_a']['stats']['count']}")
        print(f"  Series B count: {comparison['series_b']['stats']['count']}")
        print(f"  Mean A: {comparison['series_a']['stats']['mean']}")
        print(f"  Mean B: {comparison['series_b']['stats']['mean']}")
        print(f"  Mean difference: {comparison['comparison']['mean_difference']}")
    except Exception as e:
        print(f"Error comparing metric series: {e}")
