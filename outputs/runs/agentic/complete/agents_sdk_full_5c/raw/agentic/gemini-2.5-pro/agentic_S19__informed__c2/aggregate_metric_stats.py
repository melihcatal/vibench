from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id

def get_aggregated_metric(
    metric_type: str,
    aggregation_alignment: monitoring_v3.Aggregation.Aligner,
    minutes_ago: int = 60,
):
    """
    Retrieves aggregated statistics for a metric over a time window.
    
    Args:
        metric_type: The full name of the metric, e.g., "compute.googleapis.com/instance/cpu/utilization".
        aggregation_alignment: The alignment function, e.g., ALIGN_MEAN, ALIGN_MAX.
        minutes_ago: The duration of the window in minutes.
    """
    client = get_monitoring_client()
    project_name = f"projects/{get_project_id()}"
    
    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(now.timestamp())},
        }
    )
    
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": minutes_ago * 60},
            "per_series_aligner": aggregation_alignment,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_NONE,
        }
    )

    request = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": aggregation,
    }

    results = client.list_time_series(request=request)
    
    # Simplified: return raw results for demonstration
    return list(results)
