from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_observability_client
from observability_models import MetricStatsRequest, MetricStatsResponse


def aggregate_metric_stats(request: MetricStatsRequest) -> MetricStatsResponse:
    client = get_observability_client()
    project_name = f"projects/{client.project_id}"
    
    query = (
        f"fetch gcp_metric"
        f" | metric type='{request.metric_name}'"
        f" | filter resource.labels.project_id = '{client.project_id}'"
        f" | align rate({request.window_hours}h)"
        f" | every {request.window_hours}h"
        f" | group_by [resource.labels], [value_mean: mean(value)]"
    )
    
    result = client.query_time_series(name=project_name, query=query)
    
    stats = MetricStatsResponse(
        metric_name=request.metric_name,
        window_hours=request.window_hours,
        stats=[]
    )
    
    for series in result.time_series:
        for point in series.points:
            stats.stats.append({
                "timestamp": point.interval.end_time.ToDatetime(),
                "mean": float(point.value.double_value),
                "resource_labels": dict(series.resource.labels)
            })
    
    return stats