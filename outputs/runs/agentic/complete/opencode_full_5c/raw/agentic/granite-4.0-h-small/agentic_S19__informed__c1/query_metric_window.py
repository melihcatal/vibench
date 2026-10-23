# query_metric_window.py
# SAME-SCENARIO: Query recent datapoints for a named metric over a time window

from observability_client import ObservabilityClient
from observability_models import QueryRequest, QueryResponse


def query_metric_window(
    metric: str, start_time: str = None, end_time: str = None, window: str = "P1H"
) -> QueryResponse:
    """Retrieve raw datapoints for `metric` within the specified time window.

    Args:
        metric: The metric name (e.g., "cpu.usage").
        start_time: Optional ISO‑8601 start timestamp.
        end_time: Optional ISO‑8601 end timestamp.
        window: Relative window string (e.g., "P1H" for one hour). If both
                `start_time` and `end_time` are omitted, this window is used.

    Returns:
        A `QueryResponse` containing normalized datapoints.
    """
    client = ObservabilityClient()

    # Build the request payload using the helper model
    payload = QueryRequest(
        metric=metric, start_time=start_time, end_time=end_time, window=window
    )
    resp = client.request("GET", "/api/v1/query", json=payload.to_dict())
    # The client returns a provider‑specific dict; wrap it in our normalized object
    return QueryResponse(resp)


# Example CLI usage (for local testing only)
if __name__ == "__main__":
    result = query_metric_window(metric="cpu.usage", window="P30M")
    print("Normalized datapoints:", result.data)
