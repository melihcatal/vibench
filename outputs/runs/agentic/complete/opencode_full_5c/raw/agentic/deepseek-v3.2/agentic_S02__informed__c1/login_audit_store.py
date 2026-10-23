import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from google.cloud import firestore


def store_audit_record(audit_data: Dict[str, Any]) -> str:
    google_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not google_credentials:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    db = firestore.Client()

    audit_data["timestamp"] = datetime.utcnow().isoformat()
    audit_data["stored_at"] = firestore.SERVER_TIMESTAMP

    doc_ref = db.collection("federated_login_audits").document()
    doc_ref.set(audit_data)

    return doc_ref.id


def get_audit_records(
    user_id: Optional[str] = None, limit: int = 100
) -> List[Dict[str, Any]]:
    google_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not google_credentials:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    db = firestore.Client()

    query = db.collection("federated_login_audits").order_by(
        "timestamp", direction=firestore.Query.DESCENDING
    )

    if user_id:
        query = query.where("user_id", "==", user_id)

    query = query.limit(limit)

    docs = query.stream()

    records = []
    for doc in docs:
        record = doc.to_dict()
        record["id"] = doc.id
        records.append(record)

    return records


def update_audit_record(record_id: str, updates: Dict[str, Any]) -> bool:
    google_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not google_credentials:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    db = firestore.Client()

    doc_ref = db.collection("federated_login_audits").document(record_id)

    updates["updated_at"] = firestore.SERVER_TIMESTAMP

    try:
        doc_ref.update(updates)
        return True
    except Exception:
        return False
