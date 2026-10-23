# SAME-SCENARIO: compare_metric_series.py
from observability_client import MetricsClient
from observability_models import MetricSeriesRequest

def compare_metric_series(resource_a: str, resource_b: str, metric_name: str, start: str, end: str):
    # Build a request to fetch metric series for both resources over the same window.
    request = MetricSeriesRequest(
        metric=metric_name,
        start=start,
        end=end,
        resources=[resource_a, resource_b],
    )
    return MetricsClient.get().query(request)

if __name__ == "__main__":
    # Azure Monitor Metrics example (set AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)
    series = compare_metric_series(
        "/subscriptions/123/resourceGroups/rg1/providers/Microsoft.Compute/virtualMachines/vmA",
        "subscriptions/123/resourceGroups/rg1/providers/Microsoft.Compute/virtualMachines/vmB",
        "Microsoft.Compute/virtualMachines/cpuPercentage",
        "2025-08-01T12:00:00Z",
        "2025-08-01T13:00:00Z",
    )
    print(series)
