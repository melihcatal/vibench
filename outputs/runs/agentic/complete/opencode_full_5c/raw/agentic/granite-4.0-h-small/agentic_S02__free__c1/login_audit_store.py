# login_audit_store.py
# [LATER-STEP] Persist federated-login audit records in a managed document store (e.g., MongoDB)

import json
from typing import List, Dict, Any

from identity_models import AuditEvent


# Simulated client for a managed document store (e.g., MongoDB, DynamoDB, etc.)
class DocumentStoreClient:
    def __init__(self, db_name: str = "login_audit", collection_name: str = "events"):
        # In production you would connect using official SDKs; here we just keep an in‑memory list.
        self.db_name = db_name
        self.collection_name = collection_name
        self.store: List[Dict[str, Any]] = []

    def insert_one(self, doc: Dict[str, Any]) -> None:
        """Insert a single audit event document."""
        self.store.append(doc)

    def insert_many(self, docs: List[Dict[str, Any]]) -> None:
        """
        Insert multiple audit events atomically (batch write).
        This mimics bulk insert APIs of real providers.
        """
        self.store.extend(docs)

    def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Simple in‑memory filter for demo purposes
        return [
            doc for doc in self.store if all(doc.get(k) == v for k, v in query.items())
        ]

    def count(self, query: Dict[str, Any] = {}) -> int:
        return len(self.find(query))


def audit_store(events: List[AuditEvent], client: DocumentStoreClient) -> None:
    """Transform AuditEvent objects into storage‑ready dicts and write them."""
    storage_records = [ev.to_dict() for ev in events]
    client.insert_many(storage_records)


def recent_audit_query(
    client: DocumentStoreClient, days_back: int = 7
) -> List[Dict[str, Any]]:
    """Retrieve audit events from the last N days (demo uses simple timestamp format)."""
    now_iso = datetime.utcnow().isoformat() + "Z"
    # Convert stored timestamps back to datetime for comparison
    import datetime

    threshold = (
        datetime.datetime.utcnow() - datetime.timedelta(days=days_back)
    ).isoformat() + "Z"
    return [doc for doc in client.store if doc["timestamp"] >= threshold]


if __name__ == "__main__":
    # Demo setup
    client = DocumentStoreClient()
    # Create some example AuditEvents
    events = [
        AuditEvent(
            event_id="e1",
            timestamp="2024-01-01T10:00:00Z",
            user_id="user-1",
            provider="google",
            action="login_success",
            details={"method": "pkce"},
        ),
        AuditEvent(
            event_id="e2",
            timestamp="2024-01-02T12:30:00Z",
            user_id="user-2",
            provider="okta",
            action="login_failure",
            details={"error_code": 401},
        ),
    ]
    # Persist the events
    audit_store(events, client)
    # Verify we can read them back
    print("All stored events:", json.dumps(client.store, indent=2))
    # Retrieve recent events (default 7 days)
    print(
        "Recent events:", json.dumps(recent_audit_query(client, days_back=1), indent=2)
    )
