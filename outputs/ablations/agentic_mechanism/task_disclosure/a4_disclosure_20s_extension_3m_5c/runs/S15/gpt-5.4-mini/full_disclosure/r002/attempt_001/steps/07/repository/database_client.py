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


def load_database_config() -> DatabaseConfig:
    table_name = os.getenv("DYNAMODB_TABLE_NAME") or os.getenv("AWS_DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("Missing DYNAMODB_TABLE_NAME")
    return DatabaseConfig(
        table_name=table_name,
        primary_key=os.getenv("DYNAMODB_PRIMARY_KEY", "id"),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT_URL") or os.getenv("AWS_DYNAMODB_ENDPOINT_URL"),
    )


def create_dynamodb_resource(config: Optional[DatabaseConfig] = None):
    cfg = config or load_database_config()
    kwargs: Dict[str, Any] = {}
    if cfg.region_name:
        kwargs["region_name"] = cfg.region_name
    if cfg.endpoint_url:
        kwargs["endpoint_url"] = cfg.endpoint_url
    return boto3.resource("dynamodb", **kwargs)


def get_table_name(config: Optional[DatabaseConfig] = None) -> str:
    return (config or load_database_config()).table_name


def get_primary_key_name(config: Optional[DatabaseConfig] = None) -> str:
    return (config or load_database_config()).primary_key
