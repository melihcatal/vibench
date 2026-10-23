from __future__ import annotations

import os
from typing import Dict, Optional

import boto3

from observability_models import MetricWindowRequest


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def cloudwatch_client(region_name: Optional[str] = None):
    return boto3.client("cloudwatch", region_name=region_name or get_aws_region())


def s3_client(region_name: Optional[str] = None):
    return boto3.client("s3", region_name=region_name or get_aws_region())


def bedrock_runtime_client(region_name: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region_name or get_aws_region())


def amazon_translate_client(region_name: Optional[str] = None):
    return boto3.client("translate", region_name=region_name or get_aws_region())


def build_metric_request(
    metric_name: str,
    start_time,
    end_time,
    namespace: str = "AWS/EC2",
    period: int = 300,
    stat: str = "Average",
    dimensions: Optional[Dict[str, str]] = None,
    unit: Optional[str] = None,
) -> MetricWindowRequest:
    return MetricWindowRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=dimensions or {},
        unit=unit,
    )


def get_metric_statistics(request: MetricWindowRequest):
    client = cloudwatch_client()
    return client.get_metric_statistics(**request.as_cloudwatch_kwargs())
