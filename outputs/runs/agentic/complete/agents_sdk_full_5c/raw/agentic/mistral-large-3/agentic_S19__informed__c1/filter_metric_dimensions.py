from google.cloud import monitoring_v3
from observability_client import get_observability_client
from observability_models import DimensionFilterRequest, MetricDataPoint


def filter_metric_dimensions(request: DimensionFilterRequest) -> list[MetricDataPoint]:
    client = get_observability_client()
    project_name = f"projects/{client.project_id}"
    
    filter_parts = [f"metric.type='{request.metric_name}'"]
    for key, value in request.dimension_filters.items():
        filter_parts.append(f"resource.labels.{key}='{value}'")
    
    query = (
        f"fetch gcp_metric"
        f" | {' AND '.join(filter_parts)}"
        f" | align rate({request.window_hours}h)"
        f" | every {request.window_hours}h"
    )
    
    result = client.query_time_series(name=project_name, query=query)
    
    points = []
    for series in result.time_series:
        for point in series.points:
            points.append(
                MetricDataPoint(
                    timestamp=point.interval.end_time.ToDatetime(),
                    value=float(point.value.double_value),
                    resource_labels=dict(series.resource.labels)
                )
            )
    
    return points