from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Optional

from azure.cosmos import CosmosClient, PartitionKey


@dataclass(frozen=True)
class NoSQLConfig:
    endpoint: str
    key: str
    database_name: str
    container_name: str


@lru_cache(maxsize=1)
def load_config() -> NoSQLConfig:
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    database_name = os.environ.get("AZURE_COSMOS_DATABASE", "documents_db")
    container_name = os.environ.get("AZURE_COSMOS_CONTAINER", "documents")
    return NoSQLConfig(endpoint, key, database_name, container_name)


@lru_cache(maxsize=1)
def get_client() -> CosmosClient:
    cfg = load_config()
    return CosmosClient(cfg.endpoint, credential=cfg.key)


@lru_cache(maxsize=1)
def get_container():
    cfg = load_config()
    client = get_client()
    database = client.create_database_if_not_exists(id=cfg.database_name)
    return database.create_container_if_not_exists(
        id=cfg.container_name,
        partition_key=PartitionKey(path="/partition_key"),
        offer_throughput=400,
    )


def container_name() -> str:
    return load_config().container_name


def database_name() -> str:
    return load_config().database_name
