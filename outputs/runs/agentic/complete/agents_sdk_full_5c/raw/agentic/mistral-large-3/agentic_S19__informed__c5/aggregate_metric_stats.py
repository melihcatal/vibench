from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_client_config
from datetime import datetime, timedelta


def aggregate_metric_stats(metric_type: str, hours: int = 1, project_id: str = None):
    config = get_client_config()
    project_id = project_id or config.get("GOOGLE_CLOUD_PROJECT")
    
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
    
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 60},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        }
    )
    
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": query,
            "interval": interval,
            "aggregation": aggregation,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    
    stats = []
    for series in results:
        series_stats = {
            "metric": {
                "type": series.metric.type,
                "labels": dict(series.metric.labels),
            },
            "resource": {
                "type": series.resource.type,
                "labels": dict(series.resource.labels),
            },
            "aggregated_values": [],
        }
        
        for point in series.points:
            series_stats["aggregated_values"].append(
                {
                    "interval": {
                        "start_time": point.interval.start_time.ToDatetime(),
                        "end_time": point.interval.end_time.ToDatetime(),
                    },
                    "value": point.value.double_value,
                }
            )
        
        stats.append(series_stats)
    
    return stats