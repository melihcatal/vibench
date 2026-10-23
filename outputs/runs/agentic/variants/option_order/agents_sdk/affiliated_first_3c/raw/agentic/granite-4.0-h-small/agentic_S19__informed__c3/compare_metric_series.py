# compare_metric_series.py
# SAME-SCENARIO: compare metric values for two resources or dimension filters over the same window

from observability_client import ObservabilityClient
from observability_models import MetricResponse
from observability_models import MetricQueryRequest

client = ObservabilityClient()


def compare_metric_series(
    resource_id_a: str,
    metric_name_a: str,
    start_time: str,
    end_time: str,
    resource_id_b: str,
    metric_name_b: str,
    dimension_filter_a: str | None = None,
    dimension_filter_b: str | None = None,
) -> dict[str, Any]:
    """
    Retrieve metric series for two independent identifiers (different resources or dimension filters)
    and return them side‑by‑side for easy comparison.
    """
    def fetch(resource_id, metric_name, dim_filter):
        request: MetricQueryRequest = {
            "resource_id": resource_id,
            "metric_name": metric_name,
            "start_time": start_time,
            "end_time": end_time,
        }
        if dim_filter:
            request["filter"] = dim_filter
        raw = client.get_metrics(
            resource_id=resource_id,
            metric_name=metric_name,
            start_time=start_time,
            end_time=end_time,
        )
        return [normalize_metric(pt) for pt in raw]

    series_a = fetch(resource_id_a, metric_name_a, dimension_filter_a)
    series_b = fetch(resource_id_b, metric_name_b, dimension_filter_b)

    # Ensure comparable timestamps by merging keys
    timestamps_a = {pt['timestamp']: pt['value'] for pt in series_a}
    timestamps_b = {pt['timestamp']: pt['value'] for pt in series_b}
    all_ts = sorted(set(timestamps_a) | set(timestamps_b))

    comparison = {
        "resource_a": resource_id_a,
        "metric_a": metric_name_a,
        "resource_b": resource_id_b,
        "metric_b": metric_name_b,
        "comparison": [
            {
                "timestamp": ts,
                "value_a": timestamps_a.get(ts),
                "value_b": timestamps_b.get(ts)
            }
            for ts in all_ts
        ]
    }
    return comparison

# ---------------------------------------------------------------------------
# Example usage (remove or guard with __main__ when integrating into services)
if __name__ == "__main__":
    sub_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    rg = os.getenv('AZURE_RESOURCE_GROUP')
    vm1 = f"/subscriptions/{sub_id}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/vm1"
    vm2 = f"/subscriptions/{sub_id}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/vm2"
    metric = "Percentage CPU"
    now = "2025-08-15T12:00:00Z"
    later = "2025-08-15T13:00:00Z"
    result = compare_metric_series(
        vm1, metric, now, later,
        vm2, metric
    )
    print(result)
