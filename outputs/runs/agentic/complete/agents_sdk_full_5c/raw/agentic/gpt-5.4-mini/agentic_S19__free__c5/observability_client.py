from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.config import Config
from botocore.client import BaseClient


@dataclass(frozen=True)
class ObservabilityConfig:
    region_name: str
    namespace: str


_DEFAULT_NAMESPACE = os.getenv("CLOUDWATCH_NAMESPACE", "ManagedMetrics")


def load_config(namespace: Optional[str] = None) -> ObservabilityConfig:
    region_name = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return ObservabilityConfig(region_name=region_name, namespace=namespace or _DEFAULT_NAMESPACE)


def get_cloudwatch_client(region_name: Optional[str] = None) -> BaseClient:
    cfg = Config(retries={"max_attempts": 3, "mode": "standard"})
    return boto3.client("cloudwatch", region_name=region_name or load_config().region_name, config=cfg)


def get_cloudwatch_logs_client(region_name: Optional[str] = None) -> BaseClient:
    cfg = Config(retries={"max_attempts": 3, "mode": "standard"})
    return boto3.client("logs", region_name=region_name or load_config().region_name, config=cfg)


def get_s3_client(region_name: Optional[str] = None) -> BaseClient:
    cfg = Config(retries={"max_attempts": 3, "mode": "standard"})
    return boto3.client("s3", region_name=region_name or load_config().region_name, config=cfg)
