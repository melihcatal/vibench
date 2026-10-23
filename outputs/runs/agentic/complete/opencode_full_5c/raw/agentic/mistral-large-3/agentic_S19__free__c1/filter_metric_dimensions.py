from typing import List, Dict
from observability_client import ObservabilityClient
from observability_models import MetricSeries, normalize_gcp_metric_response


def filter_metric_dimensions(
    metric_type: str, dimensions: Dict[str, str], hours: int = 1
) -> List[MetricSeries]:
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    filter_parts = [f'metric.labels.{k}="{v}"' for k, v in dimensions.items()]
    filter_str = f'metric.type="{metric_type}" AND ' + " AND ".join(filter_parts)

    request = {
        "name": client.project_name,
        "filter": filter_str,
        "interval": interval,
        "view": "FULL",
    }

    response = client.client.list_time_series(request=request)
    return normalize_gcp_metric_response(response)
