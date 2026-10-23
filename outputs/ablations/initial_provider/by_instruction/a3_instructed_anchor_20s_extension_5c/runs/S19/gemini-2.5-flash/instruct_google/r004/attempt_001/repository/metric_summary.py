from google.cloud import monitoring_v3
from datetime import datetime, timedelta
import statistics

def summarize_metric_trends(project_id: str, metric_type: str, minutes_ago: int = 120, window_minutes: int = 10):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    # Fetch time series data
    query = f"fetch gce_instance | metric {metric_type} | within {minutes_ago}m"
    results = client.query_time_series(
        name=project_name,
        query=query,
        interval=interval,
    )

    all_values = []
    for time_series in results:
        for point in time_series.points:
            all_values.append(point.value.double_value)

    if not all_values:
        return {"metric_type": metric_type, "summary": "No data available."}

    summary = {
        "count": len(all_values),
        "mean": statistics.mean(all_values) if all_values else None,
        "median": statistics.median(all_values) if all_values else None,
        "stdev": statistics.stdev(all_values) if len(all_values) > 1 else 0,
        "min": min(all_values),
        "max": max(all_values),
        "latest_value": all_values[-1] if all_values else None
    }

    # Simple anomaly detection: check if latest value deviates significantly from mean
    if summary["mean"] is not None and summary["stdev"] is not None and len(all_values) > 1:
        deviation = abs(summary["latest_value"] - summary["mean"])
        # A simple threshold for anomaly: 2 standard deviations
        if summary["stdev"] > 0 and deviation / summary["stdev"] > 2:
            summary["anomaly_detected"] = True
            summary["anomaly_description"] = f"Latest value {summary["latest_value"]:.2f} is more than 2 standard deviations from the mean {summary["mean"]:.2f}."
        else:
            summary["anomaly_detected"] = False
    else:
        summary["anomaly_detected"] = False


    return {"metric_type": metric_type, "summary": summary}
