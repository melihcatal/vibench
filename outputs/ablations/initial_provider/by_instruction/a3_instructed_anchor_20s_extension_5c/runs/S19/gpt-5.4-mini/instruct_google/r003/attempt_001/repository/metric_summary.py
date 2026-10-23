from datetime import datetime, timedelta, timezone

from observability_client import GoogleCloudMonitoringClient


def metric_summary(metric_name: str, minutes: int = 120):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    client = GoogleCloudMonitoringClient()
    series = client.list_time_series(metric_name, start_time, end_time)
    values = [p.value for p in series.points]
    if not values:
        return {"metric_name": metric_name, "trend": "empty", "anomaly": False}
    latest = values[-1]
    baseline = sum(values[:-1]) / max(len(values) - 1, 1)
    return {"metric_name": metric_name, "trend": "up" if latest > baseline else "down", "anomaly": abs(latest - baseline) > baseline * 0.5 if baseline else False}
