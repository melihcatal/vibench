# Query metric data filtered by resource labels or dimensions using a concrete provider

import datetime
from observability_models import (
    MetricFilterRequest,
    FilteredSeriesResult,
    normalize_filter_response,
)
from observability_client import ObservabilityClient


def filter_metric_dimensions(
    provider: str,
    metric_name: str,
    start_relative: str = "-1h",
    end_relative: str = "now",
    dimension_filters: List[dict] = None,
    region: str = "us-east-1",
) -> FilteredSeriesResult:
    """
    Retrieve datapoints for `metric_name` where dimension labels match the supplied filters.

    :param provider: monitored service identifier (Datadog, Azure Monitor, CloudWatch, etc.)
    :param metric_name: metric identifier as understood by the provider
    :param start_relative: relative start token (e.g., "-2h")
    :param end_relative: relative end token (e.g., "now")
    :param dimension_filters: list of dicts, each representing {label: value} pairs
                              to filter on. Example: [{"host": "web-01"}, {"env": "prod"}]
    :param region: optional region/tenant identifier used by providers that require it
    :return: normalized FilteredSeriesResult containing matching time series
    """
    start_dt, end_dt = _parse_relative_times(start_relative, end_relative)

    request = MetricFilterRequest(
        metric_name, start_dt.isoformat(), end_dt.isoformat(), dimension_filters
    )

    client = ObservabilityClient(provider, region=region)
    # Build the filter query parameters; most providers accept a filter query string
    endpoint_map = {
        "Datadog": "/query?from={}&to={}&filter={}".format(
            int(start_dt.timestamp()),
            int(end_dt.timestamp()),
            ",".join([f"{k}={v}" for f in dimension_filters for k, v in f.items()]),
        ),
        "Azure Monitor": "/v1/apps/metrics/list",
        "CloudWatch": "/ListMetrics",
        "CloudMonitor": "/ListMetricData",
        "Cloud Monitoring": "/series",
        "IBM Cloud Monitoring": "/v1/metrics/filter",
    }

    filter_param = (
        dimension_filters
        and "&".join([f"{k}={v}" for f in dimension_filters for k, v in f.items()])
        or ""
    )
    response = client.request(
        "GET",
        endpoint_map[provider],
        params={
            "metric": metric_name,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "filter": filter_param,
        },
    )

    return normalize_filter_response(provider, response)


def _parse_relative_times(
    start_expr: str, end_expr: str
) -> (datetime.datetime, datetime.datetime):
    """
    Token parser (same as other modules).
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


# Simple driver to illustrate usage
if __name__ == "__main__":
    # Example: fetch CPU usage only for instances tagged with env=prod
    result = filter_metric_dimensions(
        provider="Datadog",
        metric_name="system.cpu.user",
        start_relative="-1h",
        end_relative="now",
        dimension_filters=[{"env": "prod"}],
        region="us-east-1",
    )
    print("Found", len(result.series), "time series matching filters.")
