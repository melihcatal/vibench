from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_client_config
from datetime import datetime, timedelta


def aggregate_metric_stats(metric_type: str, hours: int = 1, project_id: str = None):
    """Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    client_config = get_client_config()
    project_id = project_id or client_config.get("GOOGLE_CLOUD_PROJECT")
    
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(end_time.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )
    
    query = f"metric.type=\"{metric_type}\""
    results = client.list_time_series(
        name=project_name,
        filter_=query,
        interval=interval,
        aggregation=monitoring_v3.Aggregation(
            alignment_period={"seconds": 60},
            per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        ),
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    )
    
    stats = []
    for series in results:
        values = [point.value.double_value for point in series.points]
        if values:
            stats.append({
                "resource": series.resource.type,
                "labels": dict(series.resource.labels),
                "count": len(values),
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
            })
    
    return stats