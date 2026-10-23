# query_metric_window.py
# SAME-SCENARIO: query recent datapoints for a named metric over a time window

from observability_client import ObservabilityClient
from observability_models import MetricResponse
from observability_models import MetricQueryRequest

client = ObservabilityClient()


def query_metric_window(
    resource_id: str,
    metric_name: str,
    start_time: str,
    end_time: str,
    dimension_filter: str | None = None,
) -> MetricResponse:
    """
    Retrieve raw metric data points for a given metric over the specified window.
    The function builds a provider-specific request and normalizes the result.
    """
    request: MetricQueryRequest = {
        "resource_id": resource_id,
        "metric_name": metric_name,
        "start_time": start_time,
        "end_time": end_time,
    }
    if dimension_filter:
        # Azure uses OData $filter syntax for dimensions,
        # e.g. "Resource/resourceUri eq '/subscriptions/.../resourceGroups/rg/providers/.../vm1'"
        request["filter"] = dimension_filter
    # Call the concrete provider client
    raw_data = client.get_metrics(
        resource_id=resource_id,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
    )
    # Normalize to our common MetricResponse shape
    return {
        "cost": None,  # placeholder; provider could add cost estimates
        "data": [normalize_metric(d) for d in raw_data]
    }

# ---------------------------------------------------------------------------
# Example usage (remove or guard with __main__ when integrating into services)
if __name__ == "__main__":
    # Azure resource ID example: subscription/resourceGroup/provider/type/name
    sub_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    rg = os.getenv('AZURE_RESOURCE_GROUP')
    resource = f"/subscriptions/{sub_id}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/myVM"
    metric = "Percentage CPU"
    now = "2025-08-15T12:00:00Z"
    one_hour_later = "2025-08-15T13:00:00Z"
    result = query_metric_window(resource, metric, now, one_hour_later)
    print(result)
