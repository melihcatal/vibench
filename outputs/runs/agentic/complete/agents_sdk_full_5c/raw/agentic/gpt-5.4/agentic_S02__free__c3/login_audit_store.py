from __future__ import annotations

import os
from dataclasses import asdict

from pymongo import MongoClient

from identity_models import AuditRecord


MONGODB_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_DB_ENV = "MONGODB_ATLAS_DB"
MONGODB_COLLECTION_ENV = "MONGODB_ATLAS_COLLECTION"


def store_login_audit(record: AuditRecord) -> str:
    client = MongoClient(os.environ[MONGODB_URI_ENV], appname="federated-login-audit")
    collection = client[os.getenv(MONGODB_DB_ENV, "identity")][os.getenv(MONGODB_COLLECTION_ENV, "login_audit")]
    payload = asdict(record)
    payload["provider"] = payload.get("provider", "auth0")
    result = collection.insert_one(payload)
    return str(result.inserted_id)
