import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass(frozen=True)
class DatabaseConfig:
    table_name: str
    primary_key: str = "id"
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None


def get_database_config() -> DatabaseConfig:
    table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME") or os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("AWS_DYNAMODB_TABLE_NAME is required")
    return DatabaseConfig(
        table_name=table_name,
        primary_key=os.getenv("AWS_DYNAMODB_PRIMARY_KEY", "id"),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        endpoint_url=os.getenv("AWS_DYNAMODB_ENDPOINT_URL") or os.getenv("DYNAMODB_ENDPOINT_URL"),
    )


def create_dynamodb_resource(config: Optional[DatabaseConfig] = None):
    cfg = config or get_database_config()
    session_kwargs: Dict[str, Any] = {}
    if cfg.region_name:
        session_kwargs["region_name"] = cfg.region_name
    session = boto3.session.Session(**session_kwargs)
    resource_kwargs: Dict[str, Any] = {}
    if cfg.endpoint_url:
        resource_kwargs["endpoint_url"] = cfg.endpoint_url
    return session.resource("dynamodb", **resource_kwargs)


def get_document_table(config: Optional[DatabaseConfig] = None):
    cfg = config or get_database_config()
    return create_dynamodb_resource(cfg).Table(cfg.table_name)


def get_primary_key_name(config: Optional[DatabaseConfig] = None) -> str:
    return (config or get_database_config()).primary_key
