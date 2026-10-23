import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class DatabaseConfig:
    table_name: str
    region_name: str
    endpoint_url: Optional[str] = None
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None


def get_database_config() -> DatabaseConfig:
    table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME") or os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("Missing AWS_DYNAMODB_TABLE_NAME")
    return DatabaseConfig(
        table_name=table_name,
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1",
        endpoint_url=os.getenv("AWS_DYNAMODB_ENDPOINT_URL") or os.getenv("DYNAMODB_ENDPOINT_URL"),
        access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        session_token=os.getenv("AWS_SESSION_TOKEN"),
    )


def get_database_resource(config: Optional[DatabaseConfig] = None):
    cfg = config or get_database_config()
    session_kwargs: Dict[str, Any] = {"region_name": cfg.region_name}
    if cfg.access_key_id and cfg.secret_access_key:
        session_kwargs["aws_access_key_id"] = cfg.access_key_id
        session_kwargs["aws_secret_access_key"] = cfg.secret_access_key
    if cfg.session_token:
        session_kwargs["aws_session_token"] = cfg.session_token
    return boto3.resource("dynamodb", endpoint_url=cfg.endpoint_url, **session_kwargs)


def get_database_client(config: Optional[DatabaseConfig] = None):
    cfg = config or get_database_config()
    session_kwargs: Dict[str, Any] = {"region_name": cfg.region_name}
    if cfg.access_key_id and cfg.secret_access_key:
        session_kwargs["aws_access_key_id"] = cfg.access_key_id
        session_kwargs["aws_secret_access_key"] = cfg.secret_access_key
    if cfg.session_token:
        session_kwargs["aws_session_token"] = cfg.session_token
    return boto3.client("dynamodb", endpoint_url=cfg.endpoint_url, **session_kwargs)


def get_table_name(config: Optional[DatabaseConfig] = None) -> str:
    return (config or get_database_config()).table_name


def get_table(config: Optional[DatabaseConfig] = None):
    cfg = config or get_database_config()
    return get_database_resource(cfg).Table(cfg.table_name)


__all__ = [
    "DatabaseConfig",
    "get_database_client",
    "get_database_config",
    "get_database_resource",
    "get_table",
    "get_table_name",
]
