from datetime import datetime, timedelta, timezone

from observability_client import GoogleCloudMonitoringClient


def aggregate_metric_stats(metric_name: str, minutes: int = 60, filter_expr: str | None = None):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    client = GoogleCloudMonitoringClient()
    series = client.list_time_series(metric_name, start_time, end_time, filter_expr=filter_expr)
    values = [p.value for p in series.points]
    return {"metric_name": metric_name, "count": len(values), "sum": sum(values), "min": min(values) if values else None, "max": max(values) if values else None, "avg": (sum(values) / len(values)) if values else None}
