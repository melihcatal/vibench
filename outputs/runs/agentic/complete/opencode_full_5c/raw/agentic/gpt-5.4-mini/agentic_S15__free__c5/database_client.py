import os
from dataclasses import dataclass
from typing import Optional

import boto3
from boto3.resources.base import ServiceResource


@dataclass(frozen=True)
class DatabaseConfig:
    table_name: str
    region_name: str


def load_database_config() -> DatabaseConfig:
    table_name = os.environ["DYNAMODB_TABLE_NAME"]
    region_name = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    return DatabaseConfig(table_name=table_name, region_name=region_name)


def get_dynamodb_resource(region_name: Optional[str] = None) -> ServiceResource:
    config = load_database_config()
    return boto3.resource("dynamodb", region_name=region_name or config.region_name)


def get_table(table_name: Optional[str] = None, region_name: Optional[str] = None):
    config = load_database_config()
    resource = get_dynamodb_resource(region_name=region_name or config.region_name)
    return resource.Table(table_name or config.table_name)
