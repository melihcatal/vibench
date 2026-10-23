from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3

from observability_models import MetricQuery, MetricQueryResult, normalize_series_points


@dataclass(frozen=True)
class CloudWatchConfig:
    region_name: str
    namespace: str


@lru_cache(maxsize=1)
def load_config() -> CloudWatchConfig:
    return CloudWatchConfig(
        region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        namespace=os.getenv("CLOUDWATCH_METRIC_NAMESPACE", "ManagedMetrics/Monitoring"),
    )


@lru_cache(maxsize=1)
def cloudwatch_client():
    return boto3.client("cloudwatch", region_name=load_config().region_name)


def query_metric_data(query: MetricQuery) -> MetricQueryResult:
    client = cloudwatch_client()
    cfg = load_config()
    response = client.get_metric_statistics(
        Namespace=query.namespace or cfg.namespace,
        MetricName=query.metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in (query.dimensions or {}).items()],
        StartTime=query.start_time,
        EndTime=query.end_time,
        Period=query.period_seconds,
        Statistics=query.statistics or ["Average"],
        Unit=query.unit,
    )
    points = normalize_series_points(response.get("Datapoints", []))
    return MetricQueryResult(raw=response, points=points)


def list_dimension_names(namespace: Optional[str] = None, metric_name: Optional[str] = None) -> Dict[str, Any]:
    client = cloudwatch_client()
    cfg = load_config()
    params: Dict[str, Any] = {"Namespace": namespace or cfg.namespace}
    if metric_name:
        params["MetricName"] = metric_name
    return client.list_metrics(**params)
