import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3


@dataclass(frozen=True)
class ObservabilityConfig:
    region_name: Optional[str]
    namespace: str
    default_metric_name: Optional[str]


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        namespace=os.getenv("CLOUDWATCH_NAMESPACE", "AWS/EC2"),
        default_metric_name=os.getenv("CLOUDWATCH_METRIC_NAME"),
    )


@lru_cache(maxsize=1)
def cloudwatch_client():
    cfg = load_config()
    return boto3.client("cloudwatch", region_name=cfg.region_name)


def resolve_metric_name(metric_name: Optional[str]) -> str:
    cfg = load_config()
    return metric_name or cfg.default_metric_name or "CPUUtilization"


def build_dimensions(dimensions: Optional[Dict[str, str]]) -> list[dict[str, str]]:
    return [{"Name": key, "Value": value} for key, value in (dimensions or {}).items()]
