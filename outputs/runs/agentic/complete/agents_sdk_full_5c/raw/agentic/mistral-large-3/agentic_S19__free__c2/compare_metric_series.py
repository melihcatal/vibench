from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricComparisonResult


def compare_metric_series(
    metric_type: str, filter_a: dict, filter_b: dict, hours: int = 1
) -> MetricComparisonResult:
    """Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
    client = get_monitoring_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    def build_filter(base_filter: dict) -> str:
        parts = [f'metric.type="{metric_type}"']
        for key, value in base_filter.items():
            parts.append(f'resource.label.{key}="{value}"')
        return " AND ".join(parts)

    query_a = {
        "name": f"projects/{project_id}",
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

    query_b = {
        "name": f"projects/{project_id}",
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

    series_a = list(client.list_time_series(request=query_a))
    series_b = list(client.list_time_series(request=query_b))

    values_a = [point.value.double_value for s in series_a for point in s.points]
    values_b = [point.value.double_value for s in series_b for point in s.points]

    avg_a = sum(values_a) / len(values_a) if values_a else 0
    avg_b = sum(values_b) / len(values_b) if values_b else 0

    return MetricComparisonResult(
        series_a_avg=avg_a,
        series_b_avg=avg_b,
        difference=avg_a - avg_b,
        series_a_count=len(values_a),
        series_b_count=len(values_b),
    )