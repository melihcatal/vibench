import os
import json
import time
from typing import Any

import requests

from observability_models import (
    MetricQueryRequest,
    MetricAggregationResult,
    AggregationType,
    MetricDimensionFilter,
    MetricTimeSeries,
    MetricDataPoint,
    MetricSnapshot,
    build_datadog_query_expression,
    parse_datadog_series_response,
    normalize_timestamps,
)

DATADOG_API_BASE = "https://api.datadoghq.com/api/v1"
DATADOG_EU_API_BASE = "https://api.datadoghq.eu/api/v1"


class DatadogConfig:
    def __init__(
        self,
        api_key: str | None = None,
        app_key: str | None = None,
        site: str = "datadoghq.com",
    ):
        self.api_key = api_key or os.environ.get("DD_API_KEY", "")
        self.app_key = app_key or os.environ.get("DD_APP_KEY", "")
        self.site = site
        if site == "datadoghq.eu":
            self.api_base = DATADOG_EU_API_BASE
        else:
            self.api_base = DATADOG_API_BASE

    def is_valid(self) -> bool:
        return bool(self.api_key) and bool(self.app_key)

    def get_headers(self) -> dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }


def load_config() -> DatadogConfig:
    site = os.environ.get("DD_SITE", "datadoghq.com")
    return DatadogConfig(site=site)


def make_datadog_request(
    method: str,
    endpoint: str,
    config: DatadogConfig | None = None,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if config is None:
        config = load_config()
    if not config.is_valid():
        raise ValueError(
            "Datadog API credentials not configured. Set DD_API_KEY and DD_APP_KEY environment variables."
        )
    url = f"{config.api_base}{endpoint}"
    headers = config.get_headers()
    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        json=json_body,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def query_datadog_metrics(
    query_request: MetricQueryRequest,
    config: DatadogConfig | None = None,
) -> MetricTimeSeries:
    expression = build_datadog_query_expression(
        metric_name=query_request.metric_name,
        aggregation=query_request.aggregation,
        tags=query_request.tags if query_request.tags else None,
        rollup_seconds=query_request.interval_seconds,
    )
    start, end = normalize_timestamps(
        query_request.start_timestamp, query_request.end_timestamp
    )
    params = {
        "query": expression,
        "from": start,
        "to": end,
    }
    response_data = make_datadog_request("GET", "/query", config=config, params=params)
    return parse_datadog_series_response(response_data, query_request.metric_name)


def query_datadog_with_tags(
    filter_request: MetricDimensionFilter,
    config: DatadogConfig | None = None,
) -> MetricTimeSeries:
    expression = build_datadog_query_expression(
        metric_name=filter_request.metric_name,
        aggregation=filter_request.aggregation,
        tags=filter_request.tag_filters,
        rollup_seconds=filter_request.interval_seconds,
    )
    start, end = normalize_timestamps(
        filter_request.start_timestamp, filter_request.end_timestamp
    )
    params = {
        "query": expression,
        "from": start,
        "to": end,
    }
    response_data = make_datadog_request("GET", "/query", config=config, params=params)
    return parse_datadog_series_response(response_data, filter_request.metric_name)


def compute_aggregation_from_points(
    points: list[MetricDataPoint],
    aggregation_type: AggregationType,
) -> MetricAggregationResult:
    values = [p.value for p in points]
    if not values:
        return MetricAggregationResult(
            metric_name="",
            start_timestamp=0,
            end_timestamp=0,
            aggregation_type=aggregation_type,
            value=0.0,
        )
    result = MetricAggregationResult(
        metric_name="",
        start_timestamp=points[0].timestamp if points else 0,
        end_timestamp=points[-1].timestamp if points else 0,
        aggregation_type=aggregation_type,
        value=0.0,
        sample_count=len(values),
        min_value=min(values),
        max_value=max(values),
        avg_value=sum(values) / len(values),
        sum_value=sum(values),
    )
    if aggregation_type == AggregationType.AVG:
        result.value = result.avg_value
    elif aggregation_type == AggregationType.SUM:
        result.value = result.sum_value
    elif aggregation_type == AggregationType.MIN:
        result.value = result.min_value
    elif aggregation_type == AggregationType.MAX:
        result.value = result.max_value
    elif aggregation_type == AggregationType.COUNT:
        result.value = float(result.sample_count)
    elif aggregation_type == AggregationType.LAST:
        result.value = values[-1]
    elif aggregation_type == AggregationType.PERCENTILE_50:
        sorted_values = sorted(values)
        idx = len(sorted_values) // 2
        result.value = sorted_values[idx]
    elif aggregation_type == AggregationType.PERCENTILE_95:
        sorted_values = sorted(values)
        idx = int(len(sorted_values) * 0.95)
        result.value = sorted_values[min(idx, len(sorted_values) - 1)]
    elif aggregation_type == AggregationType.PERCENTILE_99:
        sorted_values = sorted(values)
        idx = int(len(sorted_values) * 0.99)
        result.value = sorted_values[min(idx, len(sorted_values) - 1)]
    return result


def create_snapshot(
    metric_name: str,
    time_series: MetricTimeSeries,
    aggregation_result: MetricAggregationResult | None = None,
    metadata: dict[str, str] | None = None,
) -> MetricSnapshot:
    snapshot_id = f"snapshot_{metric_name}_{int(time.time())}"
    aggregation_results = [aggregation_result] if aggregation_result else []
    return MetricSnapshot(
        snapshot_id=snapshot_id,
        metric_name=metric_name,
        start_timestamp=time_series.points[0].timestamp if time_series.points else 0,
        end_timestamp=time_series.points[-1].timestamp if time_series.points else 0,
        data=time_series.points,
        aggregation_results=aggregation_results,
        metadata=metadata or {},
        created_at=int(time.time()),
    )


def serialize_snapshot(snapshot: MetricSnapshot) -> str:
    return json.dumps(snapshot.to_dict(), indent=2)


def deserialize_snapshot(json_str: str) -> MetricSnapshot:
    data = json.loads(json_str)
    points = [
        MetricDataPoint(
            timestamp=p["timestamp"], value=p["value"], tags=p.get("tags", {})
        )
        for p in data.get("data", [])
    ]
    agg_results = []
    for r in data.get("aggregation_results", []):
        agg_results.append(
            MetricAggregationResult(
                metric_name=r["metric_name"],
                start_timestamp=r["start_timestamp"],
                end_timestamp=r["end_timestamp"],
                aggregation_type=AggregationType(r["aggregation_type"]),
                value=r["value"],
                sample_count=r.get("sample_count", 0),
                min_value=r.get("min_value", 0.0),
                max_value=r.get("max_value", 0.0),
                avg_value=r.get("avg_value", 0.0),
                sum_value=r.get("sum_value", 0.0),
                unit=r.get("unit", ""),
            )
        )
    return MetricSnapshot(
        snapshot_id=data["snapshot_id"],
        metric_name=data["metric_name"],
        start_timestamp=data["start_timestamp"],
        end_timestamp=data["end_timestamp"],
        data=points,
        aggregation_results=agg_results,
        metadata=data.get("metadata", {}),
        created_at=data.get("created_at", 0),
    )
