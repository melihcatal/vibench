import os
from dataclasses import dataclass
from functools import lru_cache

import boto3


@dataclass(frozen=True)
class ObservabilityConfig:
    region_name: str
    namespace: str
    metric_name: str


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
        namespace=os.getenv("CLOUDWATCH_NAMESPACE", "ManagedMetricsMonitoring"),
        metric_name=os.getenv("CLOUDWATCH_METRIC_NAME", "RequestCount"),
    )


@lru_cache(maxsize=1)
def cloudwatch_client():
    return boto3.client("cloudwatch", region_name=load_config().region_name)
