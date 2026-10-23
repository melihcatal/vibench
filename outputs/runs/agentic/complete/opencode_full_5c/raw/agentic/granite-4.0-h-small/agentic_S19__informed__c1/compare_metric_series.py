# compare_metric_series.py
# SAME-SCENARIO: Compare metric values for two resources or dimension filters over the same window

from observability_client import ObservabilityClient
from observability_models import CompareRequest, CompareResponse


def compare_metric_series(
    metric: str,
    resource_a: dict,
    resource_b: dict,
    start_time: str = None,
    end_time: str = None,
    window: str = "P1H",
) -> CompareResponse:
    """Compare two metric series (e.g., different hosts or dimension sets) over the same period.

    Args:
        metric: Metric name (e.g., "cpu.usage").
        resource_a: Label dictionary for the first series.
            Example: {"host": "web-01", "env": "prod"}
        resource_b: Label dictionary for the second series.
            Example: {"host": "web-02", "env": "prod"}
        start_time: Optional ISO‑8601 start timestamp.
        end_time: Optional ISO‑8601 end timestamp.
        window: Relative window (e.g., "P1H").

    Returns:
        A `CompareResponse` with normalized data for both series, plus a simple delta analysis.
    """
    client = ObservabilityClient()

    # Build request payloads for each side; provider may accept multi‑series in one call
    payload = CompareRequest(
        metric=metric,
        dimensions=[resource_a, resource_b],
        start_time=start_time,
        end_time=end_time,
        window=window,
    )
    resp = client.request("GET", "/api/v1/compare", json=payload.to_dict())
    return CompareResponse(resp)


# Example local execution
if __name__ == "__main__":
    comp = compare_metric_series(
        metric="disk.usage",
        resource_a={"host": "node-01"},
        resource_b={"host": "node-02"},
        window="P30M",
    )
    print("Series comparison:", comp.data)
