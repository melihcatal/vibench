from google.cloud import monitoring_v3
from observability_client import get_client_config
from datetime import datetime, timedelta


def compare_metric_series(metric_type: str, filter_a: dict, filter_b: dict, hours: int = 1, project_id: str = None):
    """Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
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
    
    def build_filter(filters: dict):
        parts = [f"metric.type=\"{metric_type}\""]
        for key, value in filters.items():
            parts.append(f"resource.label.{key}=\"{value}\"")
        return " AND ".join(parts)
    
    filter_query_a = build_filter(filter_a)
    filter_query_b = build_filter(filter_b)
    
    series_a = client.list_time_series(
        name=project_name,
        filter_=filter_query_a,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    )
    
    series_b = client.list_time_series(
        name=project_name,
        filter_=filter_query_b,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    )
    
    def extract_values(series):
        return [
            {
                "timestamp": point.interval.end_time.ToDatetime(),
                "value": point.value.double_value,
                "labels": dict(s.resource.labels)
            }
            for s in series
            for point in s.points
        ]
    
    return {
        "series_a": extract_values(series_a),
        "series_b": extract_values(series_b)
    }