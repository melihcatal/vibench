import os
from datetime import datetime
from typing import Any, Dict, Optional

import boto3

from observability_models import (
    MetricQuery,
    normalize_cloudwatch_datapoints,
    normalize_dimensions,
)


def _cloudwatch_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client("cloudwatch", region_name=region)


def _namespace(metric_name: str, namespace: Optional[str]) -> str:
    return namespace or os.getenv("CLOUDWATCH_NAMESPACE") or "ManagedMetricsMonitoring"


def get_metric_statistics(query: MetricQuery) -> Dict[str, Any]:
    client = _cloudwatch_client()
    kwargs: Dict[str, Any] = {
        "Namespace": _namespace(query.metric_name, query.namespace),
        "MetricName": query.metric_name,
        "StartTime": query.start_time,
        "EndTime": query.end_time,
        "Dimensions": normalize_dimensions(query.dimensions),
    }
    if query.period is not None:
        kwargs["Period"] = int(query.period)
    if query.statistic:
        kwargs["Statistics"] = [query.statistic]
    response = client.get_metric_statistics(**kwargs)
    return {
        "series": normalize_cloudwatch_datapoints(response.get("Datapoints", [])),
        "label": response.get("Label"),
    }


def get_metric_data(
    query: MetricQuery, extra_queries: Optional[list] = None
) -> Dict[str, Any]:
    client = _cloudwatch_client()
    metric_queries = [
        {
            "Id": "m1",
            "MetricStat": {
                "Metric": {
                    "Namespace": _namespace(query.metric_name, query.namespace),
                    "MetricName": query.metric_name,
                    "Dimensions": normalize_dimensions(query.dimensions),
                },
                "Period": int(query.period or 300),
                "Stat": query.statistic or "Average",
            },
            "ReturnData": True,
        }
    ]
    if extra_queries:
        metric_queries.extend(extra_queries)
    response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=query.start_time,
        EndTime=query.end_time,
    )
    return response
