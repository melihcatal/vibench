from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import DimensionFilterRequest, MetricDataPoint
from datetime import datetime, timedelta

def filter_metric_dimensions(request: DimensionFilterRequest) -> list[MetricDataPoint]:
    client = get_monitoring_client()
    project_name = f"projects/{request.project_id}"
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=request.hours)
    
    filter_parts = [f'metric.type="{request.metric_type}"']
    for key, value in request.dimensions.items():
        filter_parts.append(f'resource.labels.{key}="{value}"')
    
    query_request = {
        "name": project_name,
        "filter": " AND ".join(filter_parts),
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())}
        }
    }
    
    results = []
    for series in client.list_time_series(request=query_request):
        for point in series.points:
            results.append(
                MetricDataPoint(
                    timestamp=point.interval.end_time.ToDatetime(),
                    value=float(point.value.double_value),
                    resource_labels=dict(series.resource.labels)
                )
            )
    
    return results