from observability_client import ObservabilityClient
from observability_models import normalize_timestamp, parse_time_series_response
from datetime import datetime, timedelta


def query_metric_window(metric_name: str, hours: int = 1, filter_str: str = "") -> list:
    """Query recent datapoints for a named metric over a time window using Google Cloud Monitoring."""
    client = ObservabilityClient()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    interval = {
        "start_time": normalize_timestamp(start_time),
        "end_time": normalize_timestamp(end_time),
    }

    response = client.list_time_series(
        metric_type=metric_name,
        filter_str=filter_str,
        interval=interval,
    )

    return parse_time_series_response(response)
