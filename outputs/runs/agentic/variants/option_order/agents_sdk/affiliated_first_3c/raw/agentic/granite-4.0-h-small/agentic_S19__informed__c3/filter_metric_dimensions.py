# filter_metric_dimensions.py
# SAME-SCENARIO: query metric data filtered by resource labels or dimensions

from observability_client import ObservabilityClient
from observability_models import MetricResponse
from observability_models import MetricQueryRequest

client = ObservabilityClient()


def filter_metric_dimensions(
    resource_id: str,
    metric_name: str,
    start_time: str,
    end_time: str,
    dimension_filters: dict[str, list[str]] | None = None
) -> MetricResponse:
    """
    Retrieve metric data limited to specific dimension values (e.g., instance, status).
    Azure Monitor dimension filtering uses the $filter syntax.
    """
    request: MetricQueryRequest = {
        "resource_id": resource_id,
        "metric_name": metric_name,
        "start_time": start_time,
        "end_time": end_time,
    }
    if dimension_filters:
        # Build $filter expression for Azure: Resource/resourceUri eq '/...'
        filters = []
        for dim, vals in dimension_filters.items():
            for val in vals:
                # Azure schema: DimensionName eq 'DimensionValue'
                filters.append(f"{dim} eq '{val}'")
        # Join with AND
        request["filter"] = " and ".join(filters)
    raw = client.get_metrics(
        resource_id=resource_id,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
    )
    return {
        "raw": raw,
        "filtered": [normalize_metric(pt) for pt in raw]
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
    # Example: filter to specific instance (not typical for CPU but illustrative)
    dims = {"instance": ["myVM"]}
    result = filter_metric_dimensions(resource, metric, now, one_hour_later, dimension_filters=dims)
    print(result)
