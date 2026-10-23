from __future__ import annotations

from typing import Dict, List, Optional

from observability_client import ObservabilityClient, create_client
from observability_models import (
    MetricComparisonResult,
    MetricTimeSeries,
    compute_correlation,
    compute_diff_stats,
    normalize_datadog_series,
)


def compare_metric_series(
    metric_name: str,
    start: int,
    end: int,
    tags_a: Optional[List[str]] = None,
    tags_b: Optional[List[str]] = None,
    interval: Optional[int] = None,
    client: Optional[ObservabilityClient] = None,
) -> MetricComparisonResult:
    if client is None:
        client = create_client()

    tag_filter_a = ""
    if tags_a:
        tag_filter_a = "{" + ",".join(tags_a) + "}"
    query_a = f"{metric_name}{tag_filter_a}"

    tag_filter_b = ""
    if tags_b:
        tag_filter_b = "{" + ",".join(tags_b) + "}"
    query_b = f"{metric_name}{tag_filter_b}"

    params_a = {"from": start, "to": end, "query": query_a}
    params_b = {"from": start, "to": end, "query": query_b}
    if interval is not None:
        params_a["interval"] = interval
        params_b["interval"] = interval

    response_a = client.query_metrics_v1(
        query=query_a,
        start=start,
        end=end,
        interval=interval,
    )
    response_b = client.query_metrics_v1(
        query=query_b,
        start=start,
        end=end,
        interval=interval,
    )

    series_a_list = []
    for raw_series in response_a.get("series", []):
        series_a_list.append(normalize_datadog_series(raw_series, metric_name))

    series_b_list = []
    for raw_series in response_b.get("series", []):
        series_b_list.append(normalize_datadog_series(raw_series, metric_name))

    series_a = (
        series_a_list[0]
        if series_a_list
        else MetricTimeSeries(metric_name=metric_name, scope="")
    )
    series_b = (
        series_b_list[0]
        if series_b_list
        else MetricTimeSeries(metric_name=metric_name, scope="")
    )

    values_a = [p.value for p in series_a.points]
    values_b = [p.value for p in series_b.points]

    min_len = min(len(values_a), len(values_b))
    values_a = values_a[:min_len]
    values_b = values_b[:min_len]

    diff_values = [values_a[i] - values_b[i] for i in range(min_len)]

    diff_percent = []
    for i in range(min_len):
        if values_b[i] != 0:
            diff_percent.append((values_a[i] - values_b[i]) / abs(values_b[i]) * 100)
        else:
            diff_percent.append(0.0)

    correlation = compute_correlation(values_a, values_b)
    diff_stats = compute_diff_stats(values_a, values_b)

    return MetricComparisonResult(
        series_a=series_a,
        series_b=series_b,
        diff_values=diff_values,
        diff_percent=diff_percent,
        correlation=correlation,
        mean_diff=diff_stats["mean_diff"],
        mean_diff_percent=diff_stats["mean_diff_percent"],
        max_diff=diff_stats["max_diff"],
        min_diff=diff_stats["min_diff"],
    )
