# Query recent datapoints for a named metric over a time window using a concrete provider

import datetime
from observability_models import (
    MetricQueryRequest,
    MetricResult,
    normalize_metric_response,
)
from observability_client import ObservabilityClient


def query_metric_window(
    provider: str,
    metric_name: str,
    start_relative: str = "-1h",
    end_relative: str = "now",
    limit: int = 100,
    region: str = "us-east-1",
) -> MetricResult:
    """
    Retrieve raw datapoints for `metric_name` between the computed window.

    :param provider: name of the monitored service (e.g., Datadog, Azure Monitor, CloudWatch)
    :param metric_name: fully qualified metric identifier supported by the provider
    :param start_relative: token expression (e.g., "-1h", "-15m", "yesterday") indicating
                           how far back from now the window starts.
    :param end_relative: token expression indicating window end (usually "now" or a fixed ISO date)
    :param limit: maximum number of raw points to request (provider-specific)
    :param region: optional region/tenant identifier required by some providers
    :return: normalized MetricResult containing a list of {timestamp, value} points
    """
    # Resolve relative time strings to ISO8601 format (simplified parsing for readability)
    start_dt, end_dt = _parse_relative_times(start_relative, end_relative)

    request = MetricQueryRequest(
        metric_name, start_dt.isoformat(), end_dt.isoformat(), limit
    )

    client = ObservabilityClient(provider, region=region)
    # Example mapping of provider to endpoint path; extend as needed for each backend
    endpoint_map = {
        "Datadog": f"/query?from={int(start_dt.timestamp())}&to={int(end_dt.timestamp())}",
        "Azure Monitor": "/v1/apps/metrics/query",
        "CloudWatch": "/GetMetricData",
        "CloudMonitor": "/GetMetricData",
        "Cloud Monitoring": "",
        "IBM Cloud Monitoring": "/v1/metrics/query",
    }

    response = client.request(
        "GET",
        endpoint_map[provider],
        params={
            "metric": metric_name,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "limit": limit,
        },
    )

    # Normalizer knows how to translate provider-specific payloads into MetricResult
    return normalize_metric_response(provider, response)


def _parse_relative_times(
    start_expr: str, end_expr: str
) -> (datetime.datetime, datetime.datetime):
    """
    Simple parser that turns tokens like "-1h", "-15m", "now", "2024-01-01T00:00:00Z"
    into datetime objects relative to the current UTC time.
    """
    now = datetime.datetime.utcnow()
    if start_expr.startswith("-"):
        # e.g., "-1h" or "-15m"
        amount, unit = (
            start_expr[1:].split("m")
            if start_expr.endswith("m")
            else start_expr[1:].split("h")
        )
        amount = int(amount)
        if unit.endswith("m"):
            dt = now - datetime.timedelta(minutes=amount)
        else:
            dt = now - datetime.timedelta(hours=amount)
    else:
        # parse ISO if not relative
        dt = datetime.datetime.fromisoformat(start_expr.replace("Z", "+00:00"))
    start_dt = dt

    if end_expr.startswith("-"):
        amount, unit = (
            end_expr[1:].split("m")
            if end_expr.endswith("m")
            else end_expr[1:].split("h")
        )
        amount = int(amount)
        if unit.endswith("m"):
            dt = now - datetime.timedelta(minutes=amount)
        else:
            dt = now - datetime.timedelta(hours=amount)
    else:
        dt = datetime.datetime.fromisoformat(end_expr.replace("Z", "+00:00"))
    end_dt = dt
    return start_dt, end_dt


# Example usage (can be removed or placed in a separate test file):
if __name__ == "__main__":
    result = query_metric_window(
        provider="Datadog",
        metric_name="system.cpu.user",
        start_relative="-2h",
        end_relative="now",
        limit=200,
    )
    print(result.data[:5])  # show first five sampled points
