from observability_client import ObservabilityClient
from observability_models import normalize_timestamp, parse_time_series_response
from datetime import datetime, timedelta


def aggregate_metric_stats(
    metric_name: str, hours: int = 1, filter_str: str = "", aggregation: dict = None
) -> list:
    """Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    client = ObservabilityClient()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    interval = {
        "start_time": normalize_timestamp(start_time),
        "end_time": normalize_timestamp(end_time),
    }

    if not aggregation:
        aggregation = {
            "alignment_period": 60,
            "per_series_aligner": "ALIGN_MEAN",
            "cross_series_reducer": "REDUCE_MEAN",
        }

    response = client.list_time_series(
        metric_type=metric_name,
        filter_str=filter_str,
        interval=interval,
        aggregation=aggregation,
    )

    return parse_time_series_response(response)
