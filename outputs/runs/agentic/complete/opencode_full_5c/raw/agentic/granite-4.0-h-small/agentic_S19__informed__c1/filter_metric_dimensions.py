# filter_metric_dimensions.py
# SAME-SCENARIO: Query metric data filtered by resource labels / dimensions

from observability_client import ObservabilityClient
from observability_models import DimensionFilterRequest, FilterResponse


def filter_metric_dimensions(
    metric: str,
    dimensions: dict,
    start_time: str = None,
    end_time: str = None,
    window: str = "P1H",
) -> FilterResponse:
    """Retrieve metric datapoints that match the supplied label filters.

    Args:
        metric: Metric name (e.g., "cpu.usage").
        dimensions: Dictionary of label key/value pairs to filter on.
            Example: {"host": "web-01", "env": "prod"}
        start_time: Optional ISO‑8601 start timestamp.
        end_time: Optional ISO‑8601 end timestamp.
        window: Relative time window (e.g., "P1H").

    Returns:
        A `FilterResponse` containing normalized datapoints that satisfy the
        label constraints.
    """
    client = ObservabilityClient()

    # Assemble the filtered query request
    payload = DimensionFilterRequest(
        metric=metric,
        dimensions=dimensions,
        start_time=start_time,
        end_time=end_time,
        window=window,
    )
    resp = client.request("GET", "/api/v1/filter", json=payload.to_dict())
    return FilterResponse(resp)


# Example usage (for local testing)
if __name__ == "__main__":
    filtered = filter_metric_dimensions(
        metric="disk.io", dimensions={"device": "sda", "type": "ssd"}, window="P15M"
    )
    print("Filtered datapoints:", filtered.data)
