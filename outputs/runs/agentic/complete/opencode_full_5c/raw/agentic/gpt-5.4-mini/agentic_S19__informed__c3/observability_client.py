import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class ObservabilityConfig:
    region_name: Optional[str] = None
    namespace: Optional[str] = None


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        namespace=os.getenv("CLOUDWATCH_NAMESPACE"),
    )


def cloudwatch_client(config: Optional[ObservabilityConfig] = None):
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.region_name:
        kwargs["region_name"] = cfg.region_name
    return boto3.client("cloudwatch", **kwargs)


def metric_namespace(config: Optional[ObservabilityConfig] = None) -> str:
    cfg = config or load_config()
    return cfg.namespace or "ManagedMetrics/Monitoring"
