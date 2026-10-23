from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_monitoring_client
from observability_models import MetricStatsRequest, MetricStatsResponse
from datetime import datetime, timedelta

def aggregate_metric_stats(request: MetricStatsRequest) -> MetricStatsResponse:
    client = get_monitoring_client()
    project_name = f"projects/{request.project_id}"
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=request.hours)
    
    aggregation = {
        "alignment_period": {"seconds": 60},
        "per_series_aligner": metric_service_v3.Aggregation.Aligner.ALIGN_MEAN,
        "cross_series_reducer": metric_service_v3.Aggregation.Reducer.REDUCE_MEAN,
        "group_by_fields": request.group_by_fields
    }
    
    query_request = {
        "name": project_name,
        "filter": f'metric.type="{request.metric_type}"',
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())}
        },
        "aggregation": aggregation
    }
    
    response = client.list_time_series(request=query_request)
    stats = []
    
    for series in response:
        for point in series.points:
            stats.append({
                "timestamp": point.interval.end_time.ToDatetime(),
                "mean": point.value.double_value,
                "min": point.value.double_value,
                "max": point.value.double_value
            })
    
    return MetricStatsResponse(stats=stats)