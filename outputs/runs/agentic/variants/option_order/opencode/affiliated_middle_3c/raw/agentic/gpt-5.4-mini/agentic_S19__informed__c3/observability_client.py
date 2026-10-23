import os
from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class ObservabilityConfig:
    region_name: str
    namespace: str


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
        namespace=os.getenv("CLOUDWATCH_NAMESPACE", "ManagedMetrics"),
    )


def cloudwatch_client():
    cfg = load_config()
    return boto3.client("cloudwatch", region_name=cfg.region_name)
