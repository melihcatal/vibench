from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from boto3.resources.base import ServiceResource
from botocore.client import BaseClient


@dataclass(frozen=True)
class DatabaseConfig:
    region_name: Optional[str]
    table_name: str
    primary_key: str = "id"
    endpoint_url: Optional[str] = None


def _env(*names: str, default: Optional[str] = None) -> Optional[str]:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


def load_database_config() -> DatabaseConfig:
    table_name = _env("AWS_DDB_TABLE_NAME", "DDB_TABLE_NAME", "DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("AWS_DDB_TABLE_NAME is required")
    return DatabaseConfig(
        region_name=_env("AWS_REGION", "AWS_DEFAULT_REGION"),
        table_name=table_name,
        primary_key=_env("AWS_DDB_PRIMARY_KEY", "DDB_PRIMARY_KEY", "DYNAMODB_PRIMARY_KEY", default="id") or "id",
        endpoint_url=_env("AWS_DDB_ENDPOINT_URL", "DDB_ENDPOINT_URL", "DYNAMODB_HTTP_BASE_URL"),
    )


def create_boto3_session(region_name: Optional[str] = None) -> boto3.session.Session:
    return boto3.session.Session(region_name=region_name or _env("AWS_REGION", "AWS_DEFAULT_REGION"))


def create_dynamodb_resource(config: Optional[DatabaseConfig] = None) -> ServiceResource:
    cfg = config or load_database_config()
    return boto3.resource("dynamodb", region_name=cfg.region_name, endpoint_url=cfg.endpoint_url)


def create_dynamodb_client(config: Optional[DatabaseConfig] = None) -> BaseClient:
    cfg = config or load_database_config()
    session = create_boto3_session(cfg.region_name)
    return session.client("dynamodb", endpoint_url=cfg.endpoint_url)


def get_dynamodb_table(config: Optional[DatabaseConfig] = None):
    cfg = config or load_database_config()
    return create_dynamodb_resource(cfg).Table(cfg.table_name)


def default_identifier_key(config: Optional[DatabaseConfig] = None) -> str:
    return (config or load_database_config()).primary_key


def build_document_key(identifier: Any, config: Optional[DatabaseConfig] = None) -> Dict[str, Any]:
    return {default_identifier_key(config): identifier}
