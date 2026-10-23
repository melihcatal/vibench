# message_audit_store.py
import os
from typing import Dict, Any
from google.cloud import firestore

# Firestore credentials are picked up from env var GOOGLE_APPLICATION_CREDENTIALS


def store_audit_record(record: Dict[str, Any]) -> None:
    """Persist a processed message audit record to Firestore.",
    The record is stored under a collection named 'processed_messages'.
    """
    db = firestore.Client()
    doc_ref = db.collection("processed_messages").document(record.get("event_id"))
    doc_ref.set(record)
    print(f"Stored audit record for {record.get('event_id')} in Firestore")


# Helper to normalize a payload before storage


def normalize_for_audit(event: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare a minimal audit snapshot from a full event dict.",
    Includes event metadata, raw payload, and a timestamp of storage.
    """
    return {
        "event_id": event.get("event_id", ""),
        "timestamp": int(event.get("timestamp", int(time.time() * 1000))),
        "payload": event.get("payload", {}),
        "status": event.get("status", "processed"),
    }


# Simple CLI demo
if __name__ == "__main__":
    import time

    sample = {
        "event_id": "audit-demo-001",
        "timestamp": int(time.time() * 1000),
        "payload": {"value": 123, "note": "audit sample"},
        "status": "processed",
    }
    audit = normalize_for_audit(sample)
    store_audit_record(audit)
