from typing import Any, Dict

from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

from observability_models import MetricWindowRequest, normalize_request


def compare_metric_series(metric_name: str, start_time: str, end_time: str, left_filter: Dict[str, str], right_filter: Dict[str, str]) -> Dict[str, Any]:
    left_request = normalize_request(MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=left_filter))
    right_request = normalize_request(MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=right_filter))
    client = MetricsQueryClient(DefaultAzureCredential())
    return {"left": left_request, "right": right_request, "provider": "Azure Monitor", "client": client.__class__.__name__}
