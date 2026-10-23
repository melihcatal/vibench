from google.cloud import monitoring_v3
from observability_client import get_observability_client
from observability_models import MetricComparisonRequest, MetricComparisonResponse


def compare_metric_series(request: MetricComparisonRequest) -> MetricComparisonResponse:
    client = get_observability_client()
    project_name = f"projects/{client.project_id}"
    
    def build_query(filters: dict) -> str:
        filter_parts = [f"metric.type='{request.metric_name}'"]
        for key, value in filters.items():
            filter_parts.append(f"resource.labels.{key}='{value}'")
        return " AND ".join(filter_parts)
    
    query_a = (
        f"fetch gcp_metric"
        f" | {build_query(request.filters_a)}"
        f" | align rate({request.window_hours}h)"
        f" | every {request.window_hours}h"
    )
    
    query_b = (
        f"fetch gcp_metric"
        f" | {build_query(request.filters_b)}"
        f" | align rate({request.window_hours}h)"
        f" | every {request.window_hours}h"
    )
    
    result_a = client.query_time_series(name=project_name, query=query_a)
    result_b = client.query_time_series(name=project_name, query=query_b)
    
    def extract_points(result):
        points = []
        for series in result.time_series:
            for point in series.points:
                points.append({
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "value": float(point.value.double_value),
                    "resource_labels": dict(series.resource.labels)
                })
        return points
    
    return MetricComparisonResponse(
        metric_name=request.metric_name,
        window_hours=request.window_hours,
        series_a=extract_points(result_a),
        series_b=extract_points(result_b)
    )