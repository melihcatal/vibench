# Summarize recent metric trends or anomalies using concrete provider data

import datetime
from typing import List, Dict
from observability_models import (
    MetricQueryRequest,
    MetricResult,
    normalize_metric_response,
)
from observability_client import ObservabilityClient


def summarize_metric_trends(
    provider: str,
    metric_name: str,
    start_relative: str = "-24h",
    end_relative: str = "now",
    granularity_seconds: int = 300,
    region: str = "us-east-1",
) -> Dict[str, Any]:
    """
    Produce a high‑level summary for a metric over the requested period:
    - overall average
    - variation (std dev)
    - count of datapoints
    - list of any detected simple anomalies (e.g., values > 2σ above/below the mean)

    :param provider: monitored service identifier (Datadog, Azure Monitor, CloudWatch, etc.)
    :param metric_name: fully qualified metric identifier
    :param start_relative: relative start token (e.g., "-24h")
    :param end_relative: relative end token (e.g., "now")
    :param granularity_seconds: bucket size for aggregation (default 5‑min)
    :param region: optional region/tenant identifier
    :return: dictionary containing numeric aggregates and a simple anomaly list
    """
    start_dt, end_dt = _parse_relative_times(start_relative, end_relative)
    steps = int((end_dt - start_dt).total_seconds() / granularity_seconds)

    # Retrieve raw datapoints at the requested granularity (most providers support a period param)
    request = MetricQueryRequest(
        metric_name, start_dt.isoformat(), end_dt.isoformat(), limit=steps * 2
    )
    client = ObservabilityClient(provider, region=region)
    endpoint = "/query?from={}&to={}&limit={}&granularity={}".format(
        int(start_dt.timestamp()),
        int(end_dt.timestamp()),
        steps * 2,
        granularity_seconds,
    )
    raw = client.request("GET", endpoint, params={"metric": metric_name})
    resp = normalize_metric_response(provider, raw)
    points = resp.data  # list of {timestamp, value}

    # Simple statistical summary
    values = [pt[1] for pt in points if pt[1] is not None]
    if not values:
        return {
            "provider": provider,
            "metric": metric_name,
            "window": {"start": start_dt.isoformat(), "end": end_dt.isoformat()},
            "summary": {"count": 0, "avg": None, "stddev": None, "anomalies": []},
        }

    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    stddev = variance**0.5

    # Very naive anomaly detection: > 2σ away from mean
    anomalies = [
        {"timestamp": pt[0], "value": pt[1], "detail": "|value‑mean| > 2σ"}
        for pt in points
        if abs(pt[1] - mean) > 2 * stddev
    ]

    return {
        "provider": provider,
        "metric": metric_name,
        "window": {"start": start_dt.isoformat(), "end": end_dt.isoformat()},
        "summary": {
            "count": len(values),
            "avg": mean,
            "stddev": stddev,
            "anomalies": anomalies,
        },
    }


def _parse_relative_times(
    start_expr: str, end_expr: str
) -> (datetime.datetime, datetime.datetime):
    """
    Token parser reused from earlier modules. Returns naive UTC datetimes.
    """
    now = datetime.datetime.utcnow()
    if start_expr.startswith("-"):
        amount, unit = (
            start_expr[1:].split("m")
            if start_expr.endswith("m")
            else start_expr[1:].split("h")
        )
        amount = int(amount)
        dt = now - (
            datetime.timedelta(minutes=amount)
            if unit.endswith("m")
            else datetime.timedelta(hours=amount)
        )
    else:
        dt = datetime.datetime.fromisoformat(start_expr.replace("Z", "+00:00"))
    start_dt = dt

    if end_expr.startswith("-"):
        amount, unit = (
            end_expr[1:].split("m")
            if end_expr.endswith("m")
            else end_expr[1:].split("h")
        )
        amount = int(amount)
        dt = now - (
            datetime.timedelta(minutes=amount)
            if unit.endswith("m")
            else datetime.timedelta(hours=amount)
        )
    else:
        dt = datetime.datetime.fromisoformat(end_expr.replace("Z", "+00:00"))
    end_dt = dt
    return start_dt, end_dt


# Example invocation (can be deleted or moved to a test module)
if __name__ == "__main__":
    summary = summarize_metric_trends(
        provider="Datadog",
        metric_name="system.cpu.user",
        start_relative="-6h",
        end_relative="now",
        granularity_seconds=60,
    )
    print("Summary:", summary)
