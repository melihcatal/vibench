from observability_client import ObservabilityClient
from observability_models import normalize_timestamp, parse_time_series_response
from datetime import datetime, timedelta
import statistics


def summarize_metric_trends(metric_name: str, hours: int = 24) -> dict:
    """Summarize recent metric trends or anomalies using Google Cloud Monitoring."""
    client = ObservabilityClient()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    interval = {
        "start_time": normalize_timestamp(start_time),
        "end_time": normalize_timestamp(end_time),
    }

    response = client.list_time_series(
        metric_type=metric_name,
        filter_str="",
        interval=interval,
    )

    series = parse_time_series_response(response)
    values = [point["value"] for s in series for point in s["points"]]

    if not values:
        return {"trend": "no_data", "anomalies": []}

    mean = statistics.mean(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0
    anomalies = [v for v in values if abs(v - mean) > 2 * stdev]

    return {
        "trend": "stable" if stdev < mean * 0.1 else "volatile",
        "mean": mean,
        "stdev": stdev,
        "anomalies": anomalies,
        "window": {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
    }
