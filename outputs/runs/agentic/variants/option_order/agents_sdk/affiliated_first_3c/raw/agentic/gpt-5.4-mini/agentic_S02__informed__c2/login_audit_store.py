from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient

from identity_models import ProfileClaims


class LoginAuditStore:
    def __init__(self) -> None:
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI", "mongodb://localhost:27017"))
        self.collection = self.client[os.getenv("MONGODB_ATLAS_DB", "identity")][os.getenv("MONGODB_ATLAS_COLLECTION", "login_audit")]

    def insert_event(self, event_type: str, claims: ProfileClaims | None = None, metadata: dict[str, Any] | None = None) -> str:
        document = {
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc),
            "claims": claims.raw if claims else None,
            "metadata": metadata or {},
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)
