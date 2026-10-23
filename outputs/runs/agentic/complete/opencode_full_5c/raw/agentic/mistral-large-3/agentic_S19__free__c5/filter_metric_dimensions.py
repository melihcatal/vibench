from observability_client import ObservabilityClient
from observability_models import (
    normalize_timestamp,
    parse_time_series_response,
    build_filter_from_dimensions,
)
from datetime import datetime, timedelta


def filter_metric_dimensions(
    metric_name: str, dimensions: dict, hours: int = 1
) -> list:
    """Query metric data filtered by resource labels or dimensions using Google Cloud Monitoring."""
    client = ObservabilityClient()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    interval = {
        "start_time": normalize_timestamp(start_time),
        "end_time": normalize_timestamp(end_time),
    }

    filter_str = build_filter_from_dimensions(dimensions)

    response = client.list_time_series(
        metric_type=metric_name,
        filter_str=filter_str,
        interval=interval,
    )

    return parse_time_series_response(response)
