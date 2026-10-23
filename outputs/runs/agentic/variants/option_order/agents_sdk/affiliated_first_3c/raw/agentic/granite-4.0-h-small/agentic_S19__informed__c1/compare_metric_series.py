# compare_metric_series.py
import os
from observability_client import ManagedMetricsClient
from observability_models import CompareMetricRequest, CompareMetricResponse

# Concrete provider: IBM Cloud Monitoring
# Required env vars: IBM_CLOUD_API_KEY, IBM_MONITORING_INSTANCE_ID

def compare_metric_series(
    resource_1: str,
    resource_2: str,
    metric_name: str,
    start: str,
    end: str,
    tags_1: list[str] = None,
    tags_2: list[str] = None
) -> CompareMetricResponse:
    """Compare metric values for two resources or dimension filters over the same window.
    
    Args:
        resource_1: Identifier for the first resource (e.g., "host:my-vm-01").
        resource_2: Identifier for the second resource (e.g., "host:my-vm-02").
        metric_name: Metric identifier (e.g., "cpu.usage.percent").
        start: ISO8601 start timestamp.
        end: ISO8601 end timestamp.
        tags_1: Additional tags for the first series (optional).
        tags_2: Additional tags for the second series (optional).
    
    Returns:
        CompareMetricResponse with the two series and a simple delta analysis.
    """
    client = ManagedMetricsClient()
    request = CompareMetricRequest(
        resource_a=resource_1,
        resource_b=resource_2,
        metric=metric_name,
        start=start,
        end=end,
        tags_a=tags_1 or [],
        tags_b=tags_2 or []
    )
    response = client.compare_metrics(request)
    return response

if __name__ == "__main__":
    # Example: compare CPU usage between two VM hosts
    comp = compare_metric_series(
        resource_1="host:web-01",
        resource_2="host:web-02",
        metric_name="cpu.usage.percent",
        start="2024-08-01T00:00:00Z",
        end="2024-08-02T00:00:00Z"
    )
    print(comp)
