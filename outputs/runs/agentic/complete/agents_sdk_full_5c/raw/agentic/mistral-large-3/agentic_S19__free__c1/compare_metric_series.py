from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_client_config
from observability_models import MetricComparisonResult


def compare_metric_series(
    metric_name: str, 
    filter_a: dict[str, str],
    filter_b: dict[str, str],
    hours: int = 1,
) -> MetricComparisonResult:
    """Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
    client_config = get_client_config()
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{client_config['project_id']}"

    def build_filter(base_filter: dict[str, str]) -> str:
        parts = [f'metric.type="{metric_name}"']
        for key, value in base_filter.items():
            parts.append(f'metric.labels.{key}="{value}"')
        return " AND ".join(parts)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query_request_a = {
        "name": project_name,
        "filter": build_filter(filter_a),
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())},
        },
        "aggregation": {
            "alignment_period": {"seconds": 60},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        },
    }

    query_request_b = {
        "name": project_name,
        "filter": build_filter(filter_b),
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())},
        },
        "aggregation": {
            "alignment_period": {"seconds": 60},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        },
    }

    def extract_values(request):
        response = client.list_time_series(request=request)
        return [point.value.double_value for series in response for point in series.points]

    values_a = extract_values(query_request_a)
    values_b = extract_values(query_request_b)

    avg_a = sum(values_a) / len(values_a) if values_a else 0.0
    avg_b = sum(values_b) / len(values_b) if values_b else 0.0

    return MetricComparisonResult(
        series_a_avg=avg_a,
        series_b_avg=avg_b,
        difference=avg_a - avg_b,
        series_a_count=len(values_a),
        series_b_count=len(values_b),
    )