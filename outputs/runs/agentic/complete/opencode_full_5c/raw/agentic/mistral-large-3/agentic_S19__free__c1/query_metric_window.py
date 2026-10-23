from typing import List
from observability_client import ObservabilityClient
from observability_models import (
    MetricQuery,
    MetricSeries,
    normalize_gcp_metric_response,
)


def query_metric_window(
    metric_type: str, hours: int = 1, filter_str: str = None
) -> List[MetricSeries]:
    client = ObservabilityClient()
    query = MetricQuery(metric_type=metric_type, filter_str=filter_str, hours=hours)
    interval = client.build_time_interval(hours)

    request = {
        "name": client.project_name,
        "filter": f'metric.type="{query.metric_type}"'
        + (f" AND {query.filter_str}" if query.filter_str else ""),
        "interval": interval,
        "view": "FULL",
    }

    response = client.client.list_time_series(request=request)
    return normalize_gcp_metric_response(response)
