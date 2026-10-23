from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricComparisonRequest, MetricComparisonResponse


def compare_metric_series(request: MetricComparisonRequest) -> MetricComparisonResponse:
    client = get_monitoring_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=request.window_hours)
    
    def _query_metric(filter_parts: list[str]) -> list[float]:
        series_request = {
            "name": f"projects/{project_id}",
            "filter": " AND ".join(filter_parts),
            "interval": {
                "start_time": {"seconds": int(start_time.timestamp())},
                "end_time": {"seconds": int(end_time.timestamp())},
            },
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.HEADERS
        }
        time_series = client.list_time_series(request=series_request)
        return [float(point.value.double_value) for series in time_series for point in series.points]
    
    filter_a = [f'metric.type="{request.metric_type}"']
    for key, value in request.filter_a.items():
        filter_a.append(f'resource.label.{key}="{value}"')
    
    filter_b = [f'metric.type="{request.metric_type}"']
    for key, value in request.filter_b.items():
        filter_b.append(f'resource.label.{key}="{value}"')
    
    values_a = _query_metric(filter_a)
    values_b = _query_metric(filter_b)
    
    return MetricComparisonResponse(
        metric_type=request.metric_type,
        window_hours=request.window_hours,
        series_a_stats={
            "count": len(values_a),
            "mean": sum(values_a) / len(values_a) if values_a else 0.0,
            "min": min(values_a) if values_a else 0.0,
            "max": max(values_a) if values_a else 0.0
        },
        series_b_stats={
            "count": len(values_b),
            "mean": sum(values_b) / len(values_b) if values_b else 0.0,
            "min": min(values_b) if values_b else 0.0,
            "max": max(values_b) if values_b else 0.0
        }
    )