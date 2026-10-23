# aggregate_metric_stats.py
# SAME-SCENARIO: retrieve aggregated statistics for a metric over a time window

from observability_client import ObservabilityClient
from observability_models import MetricResponse
from observability_models import MetricQueryRequest
import os
from typing import Any

client = ObservabilityClient()


def aggregate_metric_stats(
    resource_id: str,
    metric_name: str,
    start_time: str,
    end_time: str,
    aggregation: str = "total"
) -> dict[str, Any]:
    """
    Request aggregated statistics (e.g., total, average) from the provider.
    The function forwards the request to the concrete client and returns a
    normalized summary dict.
    """
    params = {
        "resource_id": resource_id,
        "metric_name": metric_name,
        "start_time": start_time,
        "end_time": end_time,
        "interval": "PT1M",
        # Azure Monitor uses aggregation=total|average|max|min|count
        "aggregation": aggregation
    }
    raw = client.get_metrics(
        resource_id=resource_id,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        aggregation=aggregation
    )
    # Normalization: keep first value and optionally compute a simple sum/average
    values = [point['value'] for point in raw if point['value'] is not None]
    summary = {
        "count": len(values),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "total": sum(values) if values else None,
        "average": sum(values) / len(values) if values else None
    }
    return {
        "raw": raw,
        "summary": summary
    }

# ---------------------------------------------------------------------------
# Example usage (remove or guard with __main__ when integrating into services)
if __name__ == "__main__":
    sub_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    rg = os.getenv('AZURE_RESOURCE_GROUP')
    resource = f"/subscriptions/{sub_id}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/myVM"
    metric = "Percentage CPU"
    now = "2025-08-15T12:00:00Z"
    one_hour_later = "2025-08-15T13:00:00Z"
    stats = aggregate_metric_stats(resource, metric, now, one_hour_later, aggregation="total")
    print(stats)
