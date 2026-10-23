import os
import json
from datetime import datetime
from google.cloud import firestore


def message_audit_store(message_record, collection_name="message_audit"):
    """Persist processed message records to Google Cloud Firestore for later lookup."""
    db = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project"))

    if not isinstance(message_record, dict):
        message_record = {"data": str(message_record)}

    audit_record = {
        **message_record,
        "audit_timestamp": datetime.utcnow().isoformat() + "Z",
        "stored_at": firestore.SERVER_TIMESTAMP,
    }

    if "message_id" in audit_record:
        doc_id = audit_record["message_id"]
    else:
        doc_id = f"msg_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"

    doc_ref = db.collection(collection_name).document(doc_id)
    doc_ref.set(audit_record)

    return {
        "document_id": doc_id,
        "collection": collection_name,
        "stored_at": audit_record["audit_timestamp"],
        "fields_stored": list(audit_record.keys()),
    }


def get_audit_record(document_id, collection_name="message_audit"):
    """Retrieve an audit record from Firestore."""
    db = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project"))

    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        return {"found": True, "document_id": document_id, "data": data}
    else:
        return {
            "found": False,
            "document_id": document_id,
            "error": "Document not found",
        }


def query_audit_records(field, value, collection_name="message_audit", limit=10):
    """Query audit records by field value."""
    db = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project"))

    query = db.collection(collection_name).where(field, "==", value).limit(limit)
    results = query.stream()

    records = []
    for doc in results:
        records.append({"document_id": doc.id, "data": doc.to_dict()})

    return {
        "count": len(records),
        "query": {"field": field, "value": value},
        "records": records,
    }
