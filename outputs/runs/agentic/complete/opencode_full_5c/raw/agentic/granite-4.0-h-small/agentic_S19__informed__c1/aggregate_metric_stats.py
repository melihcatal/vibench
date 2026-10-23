# aggregate_metric_stats.py
# SAME-SCENARIO: Retrieve aggregated statistics for a metric over a time window

from observability_client import ObservabilityClient
from observability_models import StatsRequest, StatResponse


def aggregate_metric_stats(
    metric: str,
    start_time: str = None,
    end_time: str = None,
    window: str = "P1H",
    aggregate: str = "avg",
) -> StatResponse:
    """Fetch aggregated statistics (e.g., average, sum, min, max) for a metric.

    Args:
        metric: Metric name (e.g., "cpu.usage").
        start_time: ISO‑8601 start timestamp (optional).
        end_time: ISO‑8601 end timestamp (optional).
        window: Relative window string (e.g., "P1H").
        aggregate: Desired aggregation function ("avg", "sum", "min", "max").

    Returns:
        A `StatResponse` with normalized statistics.
    """
    client = ObservabilityClient()

    # Build the stats request payload
    payload = StatsRequest(
        metric=metric,
        start_time=start_time,
        end_time=end_time,
        window=window,
        aggregate=aggregate,
    )
    resp = client.request("POST", "/api/v1/stats", json=payload.to_dict())
    # Normalize provider‑specific result shape into our generic model
    return StatResponse(resp)


# Example local test
if __name__ == "__main__":
    stats = aggregate_metric_stats(metric="memory.usage", aggregate="max", window="P2H")
    print("Aggregated max values:", stats.data)
