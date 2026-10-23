from typing import Any, Dict

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

from observability_models import MetricWindowRequest, normalize_request


def filter_metric_dimensions(metric_name: str, start_time: str, end_time: str, dimensions: Dict[str, str]) -> Dict[str, Any]:
    request = normalize_request(MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=dimensions))
    client = MetricsQueryClient(DefaultAzureCredential())
    return {"request": request, "provider": "Azure Monitor", "dimension_count": len(dimensions or {}), "client": client.__class__.__name__}
