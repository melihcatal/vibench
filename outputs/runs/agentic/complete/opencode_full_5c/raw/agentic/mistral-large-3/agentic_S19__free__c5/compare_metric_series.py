from observability_client import ObservabilityClient
from observability_models import (
    normalize_timestamp,
    parse_time_series_response,
    build_filter_from_dimensions,
)
from datetime import datetime, timedelta


def compare_metric_series(
    metric_name: str, filter_a: dict, filter_b: dict, hours: int = 1
) -> dict:
    """Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
    client = ObservabilityClient()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    interval = {
        "start_time": normalize_timestamp(start_time),
        "end_time": normalize_timestamp(end_time),
    }

    filter_str_a = build_filter_from_dimensions(filter_a)
    filter_str_b = build_filter_from_dimensions(filter_b)

    response_a = client.list_time_series(
        metric_type=metric_name,
        filter_str=filter_str_a,
        interval=interval,
    )

    response_b = client.list_time_series(
        metric_type=metric_name,
        filter_str=filter_str_b,
        interval=interval,
    )

    series_a = parse_time_series_response(response_a)
    series_b = parse_time_series_response(response_b)

    return {
        "series_a": series_a,
        "series_b": series_b,
        "comparison_window": {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
    }
