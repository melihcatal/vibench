from datetime import datetime

from observability_client import ObservabilityClient


def compare_metric_series(metric_name: str, start_time: datetime, end_time: datetime, left_filter: dict[str, str], right_filter: dict[str, str]):
    client = ObservabilityClient()
    payload = {
        "metric_name": metric_name,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "left_filter": left_filter,
        "right_filter": right_filter,
    }
    return client.post_json("/metrics/compare", payload)
