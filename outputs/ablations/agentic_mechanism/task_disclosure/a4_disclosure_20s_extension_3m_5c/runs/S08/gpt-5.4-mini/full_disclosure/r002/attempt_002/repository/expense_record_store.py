from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from azure.cosmos import CosmosClient


DEFAULT_COSMOS_ENDPOINT_ENV = "AZURE_COSMOS_ENDPOINT"
DEFAULT_COSMOS_KEY_ENV = "AZURE_COSMOS_KEY"
DEFAULT_COSMOS_DATABASE_ENV = "AZURE_COSMOS_DATABASE"
DEFAULT_COSMOS_CONTAINER_ENV = "AZURE_COSMOS_CONTAINER"


@dataclass(frozen=True)
class ExpenseRecordStoreConfig:
    endpoint: str
    key: str
    database: str
    container: str


def load_expense_record_store_config(env: Mapping[str, str] | None = None) -> ExpenseRecordStoreConfig:
    source = env or os.environ
    endpoint = source.get(DEFAULT_COSMOS_ENDPOINT_ENV, "")
    key = source.get(DEFAULT_COSMOS_KEY_ENV, "")
    database = source.get(DEFAULT_COSMOS_DATABASE_ENV, "expense_records")
    container = source.get(DEFAULT_COSMOS_CONTAINER_ENV, "expenses")
    if not endpoint:
        raise ValueError(f"{DEFAULT_COSMOS_ENDPOINT_ENV} is required")
    if not key:
        raise ValueError(f"{DEFAULT_COSMOS_KEY_ENV} is required")
    return ExpenseRecordStoreConfig(endpoint=endpoint, key=key, database=database, container=container)


def _normalize_record(record: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(record)
    normalized.setdefault("stored_at", datetime.now(timezone.utc).isoformat())
    if "id" not in normalized or not normalized["id"]:
        candidate = normalized.get("expense_id") or normalized.get("document_id") or normalized.get("transaction_id")
        if candidate:
            normalized["id"] = str(candidate)
    if "id" not in normalized or not normalized["id"]:
        raise ValueError("normalized expense record requires an id, expense_id, document_id, or transaction_id")
    return normalized


def create_expense_record_store(config: ExpenseRecordStoreConfig | None = None) -> tuple[Any, Any]:
    cfg = config or load_expense_record_store_config()
    client = CosmosClient(cfg.endpoint, credential=cfg.key)
    database = client.create_database_if_not_exists(id=cfg.database)
    container = database.create_container_if_not_exists(id=cfg.container, partition_key={"paths": ["/id"]})
    return client, container


def save_expense_record(record: Mapping[str, Any], config: ExpenseRecordStoreConfig | None = None) -> dict[str, Any]:
    _, container = create_expense_record_store(config)
    normalized = _normalize_record(record)
    container.upsert_item(body=normalized)
    return normalized


def get_expense_record(record_id: str, config: ExpenseRecordStoreConfig | None = None) -> dict[str, Any] | None:
    _, container = create_expense_record_store(config)
    try:
        return container.read_item(item=record_id, partition_key=record_id)
    except Exception:
        return None


__all__ = [
    "DEFAULT_COSMOS_CONTAINER_ENV",
    "DEFAULT_COSMOS_DATABASE_ENV",
    "DEFAULT_COSMOS_ENDPOINT_ENV",
    "DEFAULT_COSMOS_KEY_ENV",
    "ExpenseRecordStoreConfig",
    "create_expense_record_store",
    "get_expense_record",
    "load_expense_record_store_config",
    "save_expense_record",
]
