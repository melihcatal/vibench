import os
from observability_client import ObservabilityClient, MetricResponse
from observability_models import MetricQueryPayload


def metric_summary(metric_name, start_time, end_time):
    """Summarize recent metric trends or anomalies.

    Args:
        metric_name (str): Name of the metric.
        start_time (int): Unix timestamp for start of window (seconds).
        end_time (int): Unix timestamp for end of window (seconds).

    Returns:
        str: Human-readable summary.
    """
    client = ObservabilityClient()
    payload = MetricQueryPayload(
        metric=metric_name, start=start_time, end=end_time, window=end_time - start_time
    )
    response = client.rest_call(
        method="POST", endpoint="/api/v1/metrics/query", json=payload
    )
    normalized = MetricResponse.from_raw(response)
    if normalized.status != "ok":
        return f"Error summarizing metric: {normalized.message}"
    datapoints = normalized.data
    # Simple trend analysis
    if not datapoints:
        return "No data available for the requested window."
    values = [d[1] for d in datapoints]  # assume [timestamp, value] pairs
    avg = sum(values) / len(values)
    trend = "steady"
    if values[-1] > values[0]:
        trend = "increasing"
    elif values[-1] < values[0]:
        trend = "decreasing"
    return f"Metric {metric_name} over the past {end_time - start_time}s shows an average of {avg:.2f} and appears to be {trend}."
