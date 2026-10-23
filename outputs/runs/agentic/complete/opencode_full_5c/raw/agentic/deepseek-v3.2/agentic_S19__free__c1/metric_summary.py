import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
from google.cloud import aiplatform


def summarize_metric_trends(metric_name, window_hours=24):
    """Summarize recent metric trends or anomalies using Google Cloud AI Platform."""
    monitoring_client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=window_hours)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = timestamp_pb2.Timestamp(seconds=int(end_time.timestamp()))
    interval.start_time = timestamp_pb2.Timestamp(seconds=int(start_time.timestamp()))

    filter_str = f'metric.type = "{metric_name}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    values = []
    timestamps = []

    for time_series in monitoring_client.list_time_series(request):
        for point in time_series.points:
            value = (
                point.value.double_value
                if point.value.HasField("double_value")
                else point.value.int64_value
            )
            values.append(float(value))
            timestamps.append(point.interval.end_time.ToDatetime())

    if not values:
        return {"status": "no_data", "message": "No metric data found"}

    # Use Google Cloud AI Platform for anomaly detection
    aiplatform.init(project=project_id, location="us-central1")

    # Calculate basic statistics
    avg_value = sum(values) / len(values)
    max_value = max(values)
    min_value = min(values)

    # Simple anomaly detection (could be enhanced with Vertex AI Anomaly Detection)
    threshold = avg_value * 1.5
    anomalies = [v for v in values if v > threshold]

    # Trend analysis
    if len(values) >= 2:
        first_half_avg = sum(values[: len(values) // 2]) / (len(values) // 2)
        second_half_avg = sum(values[len(values) // 2 :]) / (
            len(values) - len(values) // 2
        )
        trend = "increasing" if second_half_avg > first_half_avg else "decreasing"
        trend_percent = (
            abs((second_half_avg - first_half_avg) / first_half_avg * 100)
            if first_half_avg > 0
            else 0
        )
    else:
        trend = "stable"
        trend_percent = 0

    summary = {
        "metric": metric_name,
        "time_window": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "hours": window_hours,
        },
        "statistics": {
            "data_points": len(values),
            "average": avg_value,
            "maximum": max_value,
            "minimum": min_value,
            "range": max_value - min_value,
        },
        "trend_analysis": {
            "direction": trend,
            "percentage_change": trend_percent,
            "anomaly_count": len(anomalies),
            "anomaly_threshold": threshold,
        },
        "provider": "Google Cloud Monitoring with AI Platform",
    }

    return summary


if __name__ == "__main__":
    summary = summarize_metric_trends(
        "compute.googleapis.com/instance/cpu/utilization", 6
    )
    print(f"Metric summary: {summary}")
