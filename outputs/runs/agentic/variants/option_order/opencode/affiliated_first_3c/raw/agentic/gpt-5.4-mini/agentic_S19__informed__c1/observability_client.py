import os
from datetime import datetime
from typing import Any, Dict, Optional

from azure.identity import DefaultAzureCredential
from azure.monitor.query import (
    MetricsQueryClient,
    MetricAggregationType,
    MetricNamespace,
)

from observability_models import normalize_metric_points, serialize_request


def get_metrics_client() -> MetricsQueryClient:
    return MetricsQueryClient(DefaultAzureCredential())


def _resource_id(resource: str) -> str:
    return resource


def _time_window(start_time: Any, end_time: Any) -> Dict[str, Any]:
    return {"start_time": start_time, "end_time": end_time}


def _agg_type(name: Optional[str]) -> Optional[MetricAggregationType]:
    if not name:
        return None
    return getattr(MetricAggregationType, name.upper(), None)


def query_metrics(
    resource: str,
    metric_name: str,
    start_time: Any,
    end_time: Any,
    granularity: Optional[str] = None,
    aggregation: Optional[str] = None,
    dimensions: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    client = get_metrics_client()
    result = client.query_resource(
        _resource_id(resource),
        metric_names=[metric_name],
        timespan=(start_time, end_time),
        granularity=granularity,
        aggregations=[_agg_type(aggregation)] if _agg_type(aggregation) else None,
        filter=dimensions,
    )
    series = []
    for metric in result.metrics:
        series.append(
            {
                "name": metric.name.value,
                "unit": str(metric.unit),
                "timeseries": [
                    normalize_metric_points(ts.data) for ts in metric.timeseries
                ],
            }
        )
    return {
        "resource": resource,
        "window": _time_window(start_time, end_time),
        "metrics": series,
    }


def compare_resource_metrics(
    resource_a: str,
    resource_b: str,
    metric_name: str,
    start_time: Any,
    end_time: Any,
    dimensions_a: Optional[Dict[str, str]] = None,
    dimensions_b: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    return {
        "left": query_metrics(
            resource_a, metric_name, start_time, end_time, dimensions=dimensions_a
        ),
        "right": query_metrics(
            resource_b, metric_name, start_time, end_time, dimensions=dimensions_b
        ),
    }
