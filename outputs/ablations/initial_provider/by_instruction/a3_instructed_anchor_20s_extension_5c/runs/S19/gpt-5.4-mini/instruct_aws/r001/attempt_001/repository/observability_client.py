import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass(frozen=True)
class ObservabilityConfig:
    aws_region: str
    namespace: str
    metric_name: str


def load_config(namespace: Optional[str] = None, metric_name: Optional[str] = None) -> ObservabilityConfig:
    return ObservabilityConfig(
        aws_region=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        namespace=namespace or os.environ.get("METRICS_NAMESPACE", "AWS/EC2"),
        metric_name=metric_name or os.environ.get("METRIC_NAME", "CPUUtilization"),
    )


def cloudwatch_client(region: Optional[str] = None):
    cfg = load_config()
    return boto3.client("cloudwatch", region_name=region or cfg.aws_region)
