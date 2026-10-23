
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, get_project_name

def get_aggregated_metric(
    metric_type: str,
    minutes_ago: int = 60,
    alignment_period_seconds: int = 600,
    aggregator: monitoring_v3.Aggregation.Aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
):
    """
    Retrieves aggregated statistics for a metric over a time window.

    Args:
        metric_type: The identifier of the metric.
        minutes_ago: The duration of the query window in minutes.
        alignment_period_seconds: The alignment period in seconds.
        aggregator: The aggregation function to apply.

    Returns:
        Aggregated time series data.
    """
    client = get_monitoring_client()
    project_name = get_project_name()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": alignment_period_seconds},
            "per_series_aligner": aggregator,
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    return list(results)
