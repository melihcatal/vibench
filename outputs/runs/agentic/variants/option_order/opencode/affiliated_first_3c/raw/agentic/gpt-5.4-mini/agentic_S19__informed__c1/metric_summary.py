from datetime import datetime, timedelta, timezone

from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def metric_summary(resource: str, metric_name: str, lookback_minutes: int = 60):
    client = MetricsQueryClient(DefaultAzureCredential())
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=lookback_minutes)
    result = client.query_resource(
        resource, metric_names=[metric_name], timespan=(start_time, end_time)
    )
    points = []
    for metric in result.metrics:
        for ts in metric.timeseries:
            points.extend(ts.data)
    values = [
        getattr(p, "average", None)
        for p in points
        if getattr(p, "average", None) is not None
    ]
    if not values:
        return {"resource": resource, "metric_name": metric_name, "status": "empty"}
    return {
        "resource": resource,
        "metric_name": metric_name,
        "min": min(values),
        "max": max(values),
        "latest": values[-1],
        "count": len(values),
    }
