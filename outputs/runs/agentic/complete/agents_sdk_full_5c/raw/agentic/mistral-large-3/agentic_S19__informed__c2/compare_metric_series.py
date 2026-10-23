from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_observability_client
from observability_models import MetricComparisonResult, MetricQueryRequest
from datetime import datetime, timedelta
from typing import List, Dict


def compare_metric_series(
    metric_type: str, 
    filter_a: Dict[str, str], 
    filter_b: Dict[str, str], 
    hours: int = 1, 
    project_id: str = None
) -> MetricComparisonResult:
    """Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
    client = get_observability_client(monitoring_v3.MetricServiceClient)
    if not project_id:
        project_id = get_observability_client("GOOGLE_CLOUD_PROJECT")

    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours)

    def build_filter(base_filter: Dict[str, str]) -> str:
        parts = [f'metric.type="{metric_type}"']
        for key, value in base_filter.items():
            parts.append(f'resource.label.{key}="{value}"')
        return " AND ".join(parts)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    def fetch_series(filter_str: str) -> List[float]:
        values = []
        for result in client.list_time_series(
            name=f"projects/{project_id}",
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
        ):
            for point in result.points:
                values.append(float(point.value.double_value))
        return values

    series_a = fetch_series(build_filter(filter_a))
    series_b = fetch_series(build_filter(filter_b))

    result = MetricComparisonResult()
    result.series_a_values = series_a
    result.series_b_values = series_b
    
    if series_a and series_b:
        result.avg_a = sum(series_a) / len(series_a)
        result.avg_b = sum(series_b) / len(series_b)
        result.diff = result.avg_a - result.avg_b

    return result