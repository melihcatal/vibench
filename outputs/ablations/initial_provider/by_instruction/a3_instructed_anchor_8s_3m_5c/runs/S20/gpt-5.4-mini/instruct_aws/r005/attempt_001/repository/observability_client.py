from __future__ import annotations

import os
from functools import lru_cache

import boto3


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    return value if value not in (None, "") else default


@lru_cache(maxsize=1)
def cloudwatch_logs_client():
    region = _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client("logs", region_name=region)


def log_group_name() -> str:
    return _env("AWS_LOG_GROUP_NAME", "/application/structured-logs")


def log_stream_name(prefix: str = "app") -> str:
    suffix = _env("HOSTNAME", "local")
    return f"{prefix}-{suffix}"


def correlation_id() -> str:
    return _env("CORRELATION_ID", "")
