from datetime import datetime

from observability_client import ObservabilityClient


def metric_summary(metric_name: str, start_time: datetime, end_time: datetime):
    client = ObservabilityClient()
    return client.post_json("/metrics/summary", {"metric_name": metric_name, "start_time": start_time.isoformat(), "end_time": end_time.isoformat(), "provider": "azure-monitor"})
