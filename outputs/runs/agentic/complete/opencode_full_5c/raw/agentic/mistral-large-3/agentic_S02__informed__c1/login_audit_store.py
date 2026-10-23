import os
from datetime import datetime
from google.cloud import firestore
from typing import Dict, Any


class FirestoreAuditStore:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection("federated_login_audits")

    def persist_audit_record(self, event: Dict[str, Any]) -> str:
        event["timestamp"] = datetime.utcnow().isoformat()
        doc_ref = self.collection.document()
        doc_ref.set(event)
        return doc_ref.id


def store_login_audit_event(
    user_id: str, event_type: str, metadata: Dict[str, Any]
) -> str:
    store = FirestoreAuditStore()
    audit_event = {"user_id": user_id, "event_type": event_type, "metadata": metadata}
    return store.persist_audit_record(audit_event)
