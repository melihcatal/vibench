from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


@dataclass(frozen=True)
class DatabaseSettings:
    region_name: Optional[str]
    endpoint_url: Optional[str]
    table_name: str


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def load_settings() -> DatabaseSettings:
    return DatabaseSettings(
        region_name=_env("AWS_REGION", _env("AWS_DEFAULT_REGION")),
        endpoint_url=_env("DYNAMODB_ENDPOINT_URL"),
        table_name=_env("DYNAMODB_TABLE_NAME", "documents") or "documents",
    )


def _client_config() -> Config:
    return Config(retries={"max_attempts": 10, "mode": "standard"})


@lru_cache(maxsize=1)
def get_dynamodb_client() -> BaseClient:
    settings = load_settings()
    kwargs: Dict[str, Any] = {"config": _client_config()}
    if settings.region_name:
        kwargs["region_name"] = settings.region_name
    if settings.endpoint_url:
        kwargs["endpoint_url"] = settings.endpoint_url
    return boto3.client("dynamodb", **kwargs)


@lru_cache(maxsize=1)
def get_table_name() -> str:
    return load_settings().table_name


def get_document_table_name(table_name: Optional[str] = None) -> str:
    return table_name or get_table_name()
