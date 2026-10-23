from typing import Any, Dict

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

from observability_models import MetricWindowRequest, normalize_request


def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str, resource_id: str = None, dimensions: Dict[str, str] = None) -> Dict[str, Any]:
    request = normalize_request(MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource_id=resource_id, dimensions=dimensions))
    client = MetricsQueryClient(DefaultAzureCredential())
    return {"request": request, "provider": "Azure Monitor", "client": client.__class__.__name__}
