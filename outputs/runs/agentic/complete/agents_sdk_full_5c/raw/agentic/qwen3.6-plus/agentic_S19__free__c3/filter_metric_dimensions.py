"""
filter_metric_dimensions.py
Queries metric data filtered by resource labels or dimensions using the Datadog API.
Provider: Datadog (api.datadoghq.com)
"""

import os
import time
from typing import List, Optional, Dict, Any

from observability_client import get_metrics_api_v1, load_datadog_config
from observability_models import (
    MetricQueryRequest,
    MetricSeries,
    normalize_datadog_series_to_metric_series,
)


def filter_metric_dimensions(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    dimension_filters: Optional[Dict[str, str]] = None,
    tag_filters: Optional[List[str]] = None,
    group_by: Optional[List[str]] = None,
    aggregation: str = "avg",
) -> List[MetricSeries]:
    """
    Query metric data filtered by resource labels/dimensions via Datadog API.

    Supports filtering by host, environment, region, service, or any custom
    Datadog tag dimension.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start of the query window in epoch seconds.
        end_ts: End of the query window in epoch seconds.
        dimension_filters: Dict of dimension key-value pairs, e.g.
            {"env": "production", "region": "us-east-1"}.
        tag_filters: Optional list of raw Datadog tag strings.
        group_by: Optional dimensions to group results by.
        aggregation: Aggregation function.

    Returns:
        List of MetricSeries, one per dimension combination.
    """
    all_tags = []

    if dimension_filters:
        for key, value in dimension_filters.items():
            all_tags.append(f"{key}:{value}")

    if tag_filters:
        all_tags.extend(tag_filters)

    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_ts,
        end_time=end_ts,
        aggregation=aggregation,
        tag_filters=all_tags if all_tags else None,
    )

    query_string = request.to_datadog_query()

    configuration = load_datadog_config()
    api = get_metrics_api_v1(configuration)
    api_client = api.api_client

    try:
        raw_response = api_client.call_api(
            resource_path="/api/v1/query",
            method="GET",
            query_params={
                "from": int(start_ts),
                "to": int(end_ts),
                "query": query_string,
            },
            response_type=dict,
        )

        if isinstance(raw_response, tuple):
            raw_response = raw_response[0]

        series_results = []
        for raw_series in raw_response.get("series", []):
            metric_series = normalize_datadog_series_to_metric_series(
                raw_series=raw_series,
                metric_name=metric_name,
                start_time=start_ts,
                end_time=end_ts,
            )

            if group_by:
                filtered_tags = {
                    k: v for k, v in (metric_series.tags or {}).items()
                    if k in group_by
                }
                metric_series.tags = filtered_tags if filtered_tags else None

            series_results.append(metric_series)

        return series_results

    except Exception as exc:
        raise RuntimeError(
            f"Datadog filter_metric_dimensions failed for metric '{metric_name}': {exc}"
        ) from exc


def filter_by_host(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    hosts: List[str],
    aggregation: str = "avg",
) -> List[MetricSeries]:
    """
    Query metric data filtered by specific hosts from Datadog.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        hosts: List of host names to include.
        aggregation: Aggregation function.

    Returns:
        List of MetricSeries per host.
    """
    return filter_metric_dimensions(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        dimension_filters={"host": f"{{{','.join(hosts)}}}"},
        aggregation=aggregation,
    )


def filter_by_environment(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    environment: str,
    aggregation: str = "avg",
) -> List[MetricSeries]:
    """
    Query metric data for a specific environment from Datadog.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        environment: Environment name, e.g. "production", "staging".
        aggregation: Aggregation function.

    Returns:
        List of MetricSeries filtered by the environment.
    """
    return filter_metric_dimensions(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        dimension_filters={"env": environment},
        aggregation=aggregation,
    )


def filter_by_service(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    service_name: str,
    additional_tags: Optional[List[str]] = None,
    aggregation: str = "avg",
) -> List[MetricSeries]:
    """
    Query metric data for a specific Datadog APM service.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        service_name: Datadog service name, e.g. "web-api", "payment-service".
        additional_tags: Optional additional tag filters.
        aggregation: Aggregation function.

    Returns:
        List of MetricSeries filtered by the service.
    """
    dimension_filters = {"service": service_name}
    return filter_metric_dimensions(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        dimension_filters=dimension_filters,
        tag_filters=additional_tags,
        aggregation=aggregation,
    )


def list_metric_dimensions(
    metric_name: str,
    start_ts: float,
    end_ts: float,
) -> Dict[str, List[str]]:
    """
    Discover available dimension values for a metric from Datadog.

    Queries the metric and extracts unique tag values per dimension key.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.

    Returns:
        Dict mapping dimension keys to lists of unique values.
    """
    series = filter_metric_dimensions(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
    )

    dimensions: Dict[str, set] = {}
    for s in series:
        if s.tags:
            for key, value in s.tags.items():
                if key not in dimensions:
                    dimensions[key] = set()
                dimensions[key].add(value)

    return {k: sorted(v) for k, v in dimensions.items()}
