import os
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import datetime
import statistics
from typing import Dict, List, Any


def summarize_metric_trends(metric_name: str, window_hours: int = 24) -> Dict[str, Any]:
    """Summarize recent metric trends or anomalies using Google Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(hours=window_hours)

    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(end_time)
    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp, start_time=start_timestamp
    )

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 3600}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN

    filter_str = f'metric.type = "{metric_name}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "aggregation": aggregation,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    hourly_values = []
    all_values = []

    for series in results:
        for point in series.points:
            value = (
                point.value.double_value
                if point.value.HasField("double_value")
                else point.value.int64_value
            )
            hourly_values.append(
                {"timestamp": point.interval.end_time.ToDatetime(), "value": value}
            )
            all_values.append(value)

    if not all_values:
        return {
            "metric": metric_name,
            "window_hours": window_hours,
            "summary": "No data available",
            "anomalies": [],
        }

    hourly_values.sort(key=lambda x: x["timestamp"])

    values_only = [v["value"] for v in hourly_values]
    mean_val = statistics.mean(values_only)
    median_val = statistics.median(values_only)
    min_val = min(values_only)
    max_val = max(values_only)

    if len(values_only) > 1:
        stdev_val = statistics.stdev(values_only)
    else:
        stdev_val = 0

    anomalies = []
    threshold_high = mean_val + (2 * stdev_val) if stdev_val > 0 else mean_val * 1.5
    threshold_low = mean_val - (2 * stdev_val) if stdev_val > 0 else mean_val * 0.5

    for i, point in enumerate(hourly_values):
        if point["value"] > threshold_high or point["value"] < threshold_low:
            anomalies.append(
                {
                    "timestamp": point["timestamp"].isoformat(),
                    "value": point["value"],
                    "deviation": abs(point["value"] - mean_val),
                    "type": "high" if point["value"] > threshold_high else "low",
                }
            )

    trend = "stable"
    if len(hourly_values) >= 2:
        first_half = values_only[: len(values_only) // 2]
        second_half = values_only[len(values_only) // 2 :]

        if len(first_half) > 0 and len(second_half) > 0:
            first_mean = statistics.mean(first_half)
            second_mean = statistics.mean(second_half)

            if second_mean > first_mean * 1.1:
                trend = "increasing"
            elif second_mean < first_mean * 0.9:
                trend = "decreasing"

    summary = {
        "metric": metric_name,
        "window_hours": window_hours,
        "summary": {
            "data_points": len(all_values),
            "series_count": len(results),
            "mean": mean_val,
            "median": median_val,
            "min": min_val,
            "max": max_val,
            "stdev": stdev_val,
            "trend": trend,
            "anomaly_count": len(anomalies),
        },
        "statistics": {
            "hourly_average": mean_val,
            "peak_value": max_val,
            "trough_value": min_val,
            "variability": stdev_val / mean_val if mean_val != 0 else 0,
        },
        "anomalies": anomalies[:10],
    }

    return summary
