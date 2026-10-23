from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import boto3

from observability_models import MetricQueryWindow


DEFAULT_NAMESPACE = os.getenv("CLOUDWATCH_NAMESPACE", "AWS/EC2")
DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def get_cloudwatch_client(region_name: Optional[str] = None):
    return boto3.client("cloudwatch", region_name=region_name or DEFAULT_REGION)


def load_metric_window(
    metric_name: str,
    namespace: Optional[str] = None,
    minutes: int = 15,
    period: int = 60,
    stat: str = "Average",
    unit: Optional[str] = None,
    dimensions: Optional[Dict[str, str]] = None,
) -> MetricQueryWindow:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    return MetricQueryWindow(
        namespace=namespace or DEFAULT_NAMESPACE,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        stat=stat,
        unit=unit,
        dimensions=dimensions or {},
    )


def build_metric_params(query: MetricQueryWindow) -> Dict[str, object]:
    params: Dict[str, object] = {
        "Namespace": query.namespace,
        "MetricName": query.metric_name,
        "StartTime": query.start_time,
        "EndTime": query.end_time,
        "Period": query.period,
        "Statistics": [query.stat],
        "Dimensions": query.to_cloudwatch_dimensions(),
    }
    if query.unit:
        params["Unit"] = query.unit
    return params
