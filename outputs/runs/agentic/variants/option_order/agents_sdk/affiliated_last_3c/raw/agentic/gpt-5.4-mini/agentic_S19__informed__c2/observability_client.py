from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import boto3

from observability_models import normalize_datetime, normalize_dimensions


@dataclass
class ObservabilityConfig:
    aws_region: str = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    namespace: str = os.getenv("CLOUDWATCH_NAMESPACE", "ManagedMetrics")
    bucket_name: str = os.getenv("METRICS_EXPORT_BUCKET", "")
    llm_model_id: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class CloudWatchMetricsClient:
    def __init__(self, config: ObservabilityConfig | None = None):
        self.config = config or ObservabilityConfig()
        self.client = boto3.client("cloudwatch", region_name=self.config.aws_region)
        self.s3 = boto3.client("s3", region_name=self.config.aws_region)

    def list_metric_data(self, *, metric_name: str, start_time, end_time, dimensions: dict[str, str] | None = None, period: int = 300, stat: str = "Average") -> dict[str, Any]:
        dims = [{"Name": k, "Value": v} for k, v in normalize_dimensions(dimensions).items()]
        return self.client.get_metric_statistics(
            Namespace=self.config.namespace,
            MetricName=metric_name,
            Dimensions=dims,
            StartTime=normalize_datetime(start_time),
            EndTime=normalize_datetime(end_time),
            Period=period,
            Statistics=[stat],
        )

    def put_object(self, *, key: str, body: bytes, content_type: str = "application/json") -> dict[str, Any]:
        return self.s3.put_object(Bucket=self.config.bucket_name, Key=key, Body=body, ContentType=content_type)
