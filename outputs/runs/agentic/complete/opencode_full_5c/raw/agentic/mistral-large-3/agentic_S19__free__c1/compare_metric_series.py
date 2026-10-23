from typing import Dict, List, Tuple
from observability_client import ObservabilityClient
from observability_models import MetricSeries, normalize_gcp_metric_response


def compare_metric_series(
    metric_type: str, filter_a: Dict[str, str], filter_b: Dict[str, str], hours: int = 1
) -> Tuple[MetricSeries, MetricSeries]:
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    def build_filter(filter_dict: Dict[str, str]) -> str:
        parts = [f'metric.labels.{k}="{v}"' for k, v in filter_dict.items()]
        return f'metric.type="{metric_type}" AND ' + " AND ".join(parts)

    request_a = {
        "name": client.project_name,
        "filter": build_filter(filter_a),
        "interval": interval,
        "view": "FULL",
    }

    request_b = {
        "name": client.project_name,
        "filter": build_filter(filter_b),
        "interval": interval,
        "view": "FULL",
    }

    response_a = client.client.list_time_series(request=request_a)
    response_b = client.client.list_time_series(request=request_b)

    series_a = normalize_gcp_metric_response(response_a)
    series_b = normalize_gcp_metric_response(response_b)

    return (
        series_a[0] if series_a else MetricSeries(metric_type=metric_type, points=[]),
        series_b[0] if series_b else MetricSeries(metric_type=metric_type, points=[]),
    )
