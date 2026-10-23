from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricStatsRequest, MetricStatsResponse


def aggregate_metric_stats(request: MetricStatsRequest) -> MetricStatsResponse:
    client = get_monitoring_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=request.window_hours)
    
    query = (
        f'fetch gcp_metric :: {request.metric_type} '
        f'| within {request.window_hours}h'
    )
    
    if request.filter_dimensions:
        filters = " && ".join([f'{k}=="{v}"' for k, v in request.filter_dimensions.items()])
        query += f' | filter {filters}'
    
    result = client.query_time_series(
        name=f"projects/{project_id}",
        query=query
    )
    
    points = [point.value.double_value for point in result.points]
    
    return MetricStatsResponse(
        metric_type=request.metric_type,
        window_hours=request.window_hours,
        count=len(points),
        mean=float(sum(points) / len(points)) if points else 0.0,
        min=min(points) if points else 0.0,
        max=max(points) if points else 0.0,
        sum=sum(points) if points else 0.0
    )