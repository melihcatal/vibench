import os
import time
import math
from typing import Any

import requests

from observability_models import (
    MetricTimeSeries,
    MetricDataPoint,
    MetricComparisonResult,
    AggregationType,
    build_datadog_query_expression,
    parse_datadog_series_response,
    normalize_timestamps,
)
from observability_client import (
    DatadogConfig,
    load_config,
    make_datadog_request,
)

DATADOG_API_BASE = "https://api.datadoghq.com/api/v1"


def _fetch_series(
    metric_name: str,
    start_timestamp: int,
    end_timestamp: int,
    tag_filters: list[str],
    aggregation: AggregationType,
    interval_seconds: int,
    config: DatadogConfig | None,
) -> MetricTimeSeries:
    expression = build_datadog_query_expression(
        metric_name=metric_name,
        aggregation=aggregation,
        tags=tag_filters if tag_filters else None,
        rollup_seconds=interval_seconds,
    )
    start, end = normalize_timestamps(start_timestamp, end_timestamp)
    if config is None:
        config = load_config()
    params = {
        "query": expression,
        "from": start,
        "to": end,
    }
    response_data = make_datadog_request("GET", "/query", config=config, params=params)
    return parse_datadog_series_response(response_data, metric_name)


def _compute_correlation(values_a: list[float], values_b: list[float]) -> float:
    n = min(len(values_a), len(values_b))
    if n < 2:
        return 0.0
    va = values_a[:n]
    vb = values_b[:n]
    mean_a = sum(va) / n
    mean_b = sum(vb) / n
    cov = sum((va[i] - mean_a) * (vb[i] - mean_b) for i in range(n)) / n
    std_a = math.sqrt(sum((v - mean_a) ** 2 for v in va) / n)
    std_b = math.sqrt(sum((v - mean_b) ** 2 for v in vb) / n)
    if std_a == 0 or std_b == 0:
        return 0.0
    return cov / (std_a * std_b)


def compare_metric_series(
    metric_name: str,
    start_timestamp: int,
    end_timestamp: int,
    tags_a: list[str],
    tags_b: list[str],
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    config: DatadogConfig | None = None,
) -> MetricComparisonResult:
    series_a = _fetch_series(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tag_filters=tags_a,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        config=config,
    )
    series_b = _fetch_series(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tag_filters=tags_b,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        config=config,
    )
    values_a = [p.value for p in series_a.points]
    values_b = [p.value for p in series_b.points]
    correlation = _compute_correlation(values_a, values_b)
    n = min(len(values_a), len(values_b))
    if n > 0:
        differences = [abs(values_a[i] - values_b[i]) for i in range(n)]
        mean_difference = sum(differences) / n
        max_difference = max(differences) if differences else 0.0
    else:
        mean_difference = 0.0
        max_difference = 0.0
    summary_parts = []
    summary_parts.append(
        f"Compared {metric_name} across two dimension sets over the query window."
    )
    summary_parts.append(f"Series A tags: {', '.join(tags_a)}")
    summary_parts.append(f"Series B tags: {', '.join(tags_b)}")
    summary_parts.append(f"Correlation: {correlation:.4f}")
    summary_parts.append(f"Mean absolute difference: {mean_difference:.4f}")
    summary_parts.append(f"Max absolute difference: {max_difference:.4f}")
    if correlation > 0.8:
        summary_parts.append("The two series are strongly positively correlated.")
    elif correlation < -0.8:
        summary_parts.append("The two series are strongly negatively correlated.")
    elif correlation > 0.5:
        summary_parts.append("The two series show moderate positive correlation.")
    else:
        summary_parts.append("The two series show weak or no correlation.")
    return MetricComparisonResult(
        series_a_name=f"{metric_name}({','.join(tags_a)})",
        series_b_name=f"{metric_name}({','.join(tags_b)})",
        series_a=series_a,
        series_b=series_b,
        correlation=correlation,
        mean_difference=mean_difference,
        max_difference=max_difference,
        summary="\n".join(summary_parts),
    )


def compare_metric_series_recent(
    metric_name: str,
    tags_a: list[str],
    tags_b: list[str],
    window_minutes: int = 60,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    config: DatadogConfig | None = None,
) -> MetricComparisonResult:
    now = int(time.time())
    start = now - (window_minutes * 60)
    return compare_metric_series(
        metric_name=metric_name,
        start_timestamp=start,
        end_timestamp=now,
        tags_a=tags_a,
        tags_b=tags_b,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        config=config,
    )


def compare_hosts(
    metric_name: str,
    host_a: str,
    host_b: str,
    start_timestamp: int,
    end_timestamp: int,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    config: DatadogConfig | None = None,
) -> MetricComparisonResult:
    return compare_metric_series(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tags_a=[f"host:{host_a}"],
        tags_b=[f"host:{host_b}"],
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        config=config,
    )


def compare_environments(
    metric_name: str,
    env_a: str,
    env_b: str,
    start_timestamp: int,
    end_timestamp: int,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    config: DatadogConfig | None = None,
) -> MetricComparisonResult:
    return compare_metric_series(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tags_a=[f"env:{env_a}"],
        tags_b=[f"env:{env_b}"],
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        config=config,
    )


if __name__ == "__main__":
    metric = os.environ.get("DD_METRIC_NAME", "system.cpu.user")
    host_a = os.environ.get("DD_HOST_A", "web-server-01")
    host_b = os.environ.get("DD_HOST_B", "web-server-02")
    window = int(os.environ.get("DD_WINDOW_MINUTES", "60"))
    result = compare_hosts(
        metric,
        host_a,
        host_b,
        start_timestamp=int(time.time()) - window * 60,
        end_timestamp=int(time.time()),
    )
    print(f"Series A: {result.series_a_name}")
    print(f"Series B: {result.series_b_name}")
    print(f"Correlation: {result.correlation:.4f}")
    print(f"Mean difference: {result.mean_difference:.4f}")
    print(f"Max difference: {result.max_difference:.4f}")
    print(f"\nSummary:\n{result.summary}")
