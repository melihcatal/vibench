from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_ATLAS_DB_ENV = "MONGODB_ATLAS_DB"
MONGODB_ATLAS_COLLECTION_ENV = "MONGODB_ATLAS_AUDIT_COLLECTION"

DEFAULT_DB = "federated_identity"
DEFAULT_COLLECTION = "login_audit_records"


def get_mongo_client() -> MongoClient:
    uri = os.getenv(MONGODB_ATLAS_URI_ENV, "")
    if not uri:
        raise ValueError(f"Environment variable {MONGODB_ATLAS_URI_ENV} is required")
    return MongoClient(uri)


def get_audit_collection(
    client: MongoClient | None = None,
    db_name: str | None = None,
    collection_name: str | None = None,
) -> Collection:
    if client is None:
        client = get_mongo_client()

    db_name = db_name or os.getenv(MONGODB_ATLAS_DB_ENV, DEFAULT_DB)
    collection_name = collection_name or os.getenv(
        MONGODB_ATLAS_COLLECTION_ENV, DEFAULT_COLLECTION
    )

    database: Database = client[db_name]
    collection: Collection = database[collection_name]
    return collection


def persist_audit_record(
    record: dict[str, Any],
    client: MongoClient | None = None,
    db_name: str | None = None,
    collection_name: str | None = None,
) -> str:
    collection = get_audit_collection(client, db_name, collection_name)

    if "_id" not in record:
        record["_id"] = record.get(
            "event_id", f"evt_{datetime.now(timezone.utc).isoformat()}"
        )

    if "created_at" not in record:
        record["created_at"] = datetime.now(timezone.utc)

    result = collection.insert_one(record)
    return str(result.inserted_id)


def persist_audit_records(
    records: list[dict[str, Any]],
    client: MongoClient | None = None,
    db_name: str | None = None,
    collection_name: str | None = None,
) -> list[str]:
    collection = get_audit_collection(client, db_name, collection_name)

    now = datetime.now(timezone.utc)
    for record in records:
        if "_id" not in record:
            record["_id"] = record.get("event_id", f"evt_{now.isoformat()}")
        if "created_at" not in record:
            record["created_at"] = now

    result = collection.insert_many(records)
    return [str(oid) for oid in result.inserted_ids]


def query_audit_records(
    query: dict[str, Any] | None = None,
    limit: int = 50,
    sort_field: str = "created_at",
    sort_order: int = -1,
    client: MongoClient | None = None,
    db_name: str | None = None,
    collection_name: str | None = None,
) -> list[dict[str, Any]]:
    collection = get_audit_collection(client, db_name, collection_name)

    cursor = collection.find(query or {}).sort(sort_field, sort_order).limit(limit)
    return list(cursor)


def build_federated_login_record(
    event_id: str,
    event_type: str,
    user_sub: str,
    client_id: str,
    provider: str = "auth0",
    connection: str = "",
    ip_address: str = "",
    user_agent: str = "",
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "event_type": event_type,
        "user_sub": user_sub,
        "client_id": client_id,
        "provider": provider,
        "connection": connection,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "details": details or {},
        "created_at": datetime.now(timezone.utc),
    }


if __name__ == "__main__":
    sample_record = build_federated_login_record(
        event_id="test_evt_001",
        event_type="login_initiated",
        user_sub="auth0|test123",
        client_id="test_client",
        provider="auth0",
        connection="google-oauth2",
        ip_address="192.168.1.1",
        details={"pkce_enabled": True},
    )
    print(f"Sample record: {sample_record}")
