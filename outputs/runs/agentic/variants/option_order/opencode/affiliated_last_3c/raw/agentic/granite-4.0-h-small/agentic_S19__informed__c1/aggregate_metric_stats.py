# Retrieve aggregated statistics for a metric over a time window using a concrete provider

import datetime
from observability_models import (
    MetricStatsRequest,
    AggregatedStatsResult,
    normalize_stats_response,
)
from observability_client import ObservabilityClient


def aggregate_metric_stats(
    provider: str,
    metric_name: str,
    start_relative: str = "-1h",
    end_relative: str = "now",
    period_seconds: int = 60,
    region: str = "us-east-1",
) -> AggregatedStatsResult:
    """
    Compute aggregated statistics (avg, sum, max, min, count) for `metric_name` within the
    requested period using the selected provider.

    :param provider: name of the monitored service (Datadog, Azure Monitor, CloudWatch, etc.)
    :param metric_name: fully qualified metric identifier supported by the provider
    :param start_relative: token expression (e.g., "-1h") for the window start
    :param end_relative: token expression (e.g., "now") for the window end
    :param period_seconds: granularity/granularity for metric aggregation (default 60s)
    :param region: optional region/tenant identifier used by some providers
    :return: normalized AggregatedStatsResult containing numeric aggregates
    """
    start_dt, end_dt = _parse_relative_times(start_relative, end_relative)

    request = MetricStatsRequest(
        metric_name, start_dt.isoformat(), end_dt.isoformat(), period_seconds
    )

    client = ObservabilityClient(provider, region=region)
    # Provider-specific endpoint; for many services the same Query endpoint works with a period param
    endpoint_map = {
        "Datadog": f"/query?from={int(start_dt.timestamp())}&to={int(end_dt.timestamp())}&aggregate={period_seconds}",
        "Azure Monitor": "/v1/apps/metrics/query",
        "CloudWatch": "/GetMetricStatistics",
        "CloudMonitor": "/GetMetricData?period={period_seconds}",
        "Cloud Monitoring": "/timeseries",
        "IBM Cloud Monitoring": "/v1/metrics/stats?period={period_seconds}",
    }

    response = client.request(
        "GET",
        endpoint_map[provider],
        params={
            "metric": metric_name,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "period": period_seconds,
        },
    )

    return normalize_stats_response(provider, response)


def _parse_relative_times(
    start_expr: str, end_expr: str
) -> (datetime.datetime, datetime.datetime):
    """
    Simple parser for relative time tokens (similar to query_metric_window).
    """
    now = datetime.datetime.utcnow()
    if start_expr.startswith("-"):
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


# Example invocation (remove or move to a test module if desired):
if __name__ == "__main__":
    stats = aggregate_metric_stats(
        provider="Datadog",
        metric_name="system.cpu.idle",
        start_relative="-30m",
        end_relative="now",
        period_seconds=60,
    )
    print(
        f"Avg={stats.avg}, Sum={stats.sum}, Max={stats.max}, Min={stats.min}, Count={stats.count}"
    )
