from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient


@dataclass(frozen=True)
class ObservabilitySettings:
    region_name: str
    namespace: str


@lru_cache(maxsize=1)
def load_settings() -> ObservabilitySettings:
    return ObservabilitySettings(
        region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        namespace=os.getenv("CLOUDWATCH_NAMESPACE", "ManagedMetricsMonitoring"),
    )


@lru_cache(maxsize=1)
def cloudwatch_client() -> BaseClient:
    return boto3.client("cloudwatch", region_name=load_settings().region_name)


def metric_dimensions(**labels: Optional[str]) -> list[dict[str, str]]:
    return [{"Name": key, "Value": value} for key, value in labels.items() if value]


def default_namespace() -> str:
    return load_settings().namespace
