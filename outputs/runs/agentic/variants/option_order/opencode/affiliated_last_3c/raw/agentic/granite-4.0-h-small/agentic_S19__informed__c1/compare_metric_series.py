# Compare metric values for two resources or dimension filters over the same window

import datetime
from typing import List, Dict
from observability_models import (
    MetricQueryRequest,
    MetricResult,
    normalize_metric_response,
)
from observability_client import ObservabilityClient


def compare_metric_series(
    provider: str,
    metric_name: str,
    resource_a: str = "hostA",
    resource_b: str = "hostB",
    start_relative: str = "-1h",
    end_relative: str = "now",
    region: str = "us-east-1",
) -> Dict[str, Dict[str, List[float]]]:
    """
    Retrieve and compare datapoints for the same metric across two distinct resources/dimension filters
    within the same time window. Returns a dictionary with raw numeric values for each resource so callers
    can compute deltas, ratios, or visualizations.

    :param provider: monitored service identifier (Datadog, Azure Monitor, CloudWatch, etc.)
    :param metric_name: metric identifier understood by the provider
    :param resource_a: label/value combination identifying the first series (e.g., host name, region, environment)
    :param resource_b: label/value combination identifying the second series
    :param start_relative: relative start token ("-2h", "-30m", etc.)
    :param end_relative: relative end token ("now" or ISO timestamp)
    :param region: optional region/tenant identifier for providers that need it
    :return: dict {resource_a: [ts, val], resource_b: [ts, val]} containing aligned points
    """
    start_dt, end_dt = _parse_relative_times(start_relative, end_relative)

    # For simplicity we request both series independently; providers that support batch queries can be
    # optimized later.
    series_a = _fetch_series(
        provider, metric_name, start_dt, end_dt, resource_a, region
    )
    series_b = _fetch_series(
        provider, metric_name, start_dt, end_dt, resource_b, region
    )

    # Align by timestamp (simple left‑to‑right merge assuming same resolution)
    aligned_a = {ts: val for ts, val in series_a}
    aligned_b = {ts: val for ts, val in series_b}

    # Build aligned result list ordered by timestamp
    ts_list = sorted(set(aligned_a.keys()) | set(aligned_b.keys()))
    return {
        resource_a: [[ts, aligned_a.get(ts, None)] for ts in ts_list],
        resource_b: [[ts, aligned_b.get(ts, None)] for ts in ts_list],
    }


def _fetch_series(
    provider: str,
    metric_name: str,
    start_dt: datetime.datetime,
    end_dt: datetime.datetime,
    label_filter: str,
    region: str,
) -> List[tuple]:
    """
    Helper that builds a one‑dimension filter dict and calls the generic filter query helper.
    """
    filter_dict = (
        {"host": label_filter}
        if provider == "Datadog"
        else {"instance_id": label_filter}
    )
    dimension_request = MetricQueryRequest(
        metric_name, start_dt.isoformat(), end_dt.isoformat(), limit=200
    )
    client = ObservabilityClient(provider, region=region)
    # Build a filter string; most providers accept label=Value form.
    filter_str = "".join([f"{k}={v}" for k, v in filter_dict.items()])
    endpoint = "/query?from={}&to={}&filter={}".format(
        int(start_dt.timestamp()), int(end_dt.timestamp()), filter_str
    )
    raw = client.request("GET", endpoint, params={"metric": metric_name})
    resp = normalize_metric_response(provider, raw)
    return [(pt[0], pt[1]) for pt in resp.data]


def _parse_relative_times(
    start_expr: str, end_expr: str
) -> (datetime.datetime, datetime.datetime):
    """
    Token parser reused from earlier modules.
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


# Example usage (remove or move to a test file if desired):
if __name__ == "__main__":
    comparison = compare_metric_series(
        provider="Datadog",
        metric_name="system.cpu.idle",
        resource_a="web-01",
        resource_b="web-02",
        start_relative="-30m",
        end_relative="now",
    )
    print("Resource A values:", comparison["hostA"][:5])
    print("Resource B values:", comparison["hostB"][:5])
