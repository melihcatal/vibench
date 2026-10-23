from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricComparisonRequest, MetricComparisonResult
from datetime import datetime, timedelta

def compare_metric_series(request: MetricComparisonRequest) -> MetricComparisonResult:
    client = get_monitoring_client()
    project_name = f"projects/{request.project_id}"
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=request.hours)
    
    def build_filter(metric_type: str, dimensions: dict) -> str:
        parts = [f'metric.type="{metric_type}"']
        for key, value in dimensions.items():
            parts.append(f'resource.labels.{key}="{value}"')
        return " AND ".join(parts)
    
    filter_a = build_filter(request.metric_type, request.dimensions_a)
    filter_b = build_filter(request.metric_type, request.dimensions_b)
    
    query_request_a = {
        "name": project_name,
        "filter": filter_a,
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())}
        }
    }
    
    query_request_b = {
        "name": project_name,
        "filter": filter_b,
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())}
        }
    }
    
    def extract_values(query_request):
        values = []
        for series in client.list_time_series(request=query_request):
            for point in series.points:
                values.append(float(point.value.double_value))
        return values
    
    values_a = extract_values(query_request_a)
    values_b = extract_values(query_request_b)
    
    return MetricComparisonResult(
        series_a_values=values_a,
        series_b_values=values_b,
        mean_a=(sum(values_a) / len(values_a)) if values_a else 0,
        mean_b=(sum(values_b) / len(values_b)) if values_b else 0
    )