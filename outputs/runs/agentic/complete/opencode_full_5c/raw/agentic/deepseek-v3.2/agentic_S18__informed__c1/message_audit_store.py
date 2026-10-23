import os
import uuid
from datetime import datetime
from google.cloud import firestore


def store_message_audit_record(
    message_data, processing_result, collection_name="message_audit"
):
    """Persist processed message records to Google Cloud Firestore for later lookup."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    db = firestore.Client(project=project_id)

    record_id = str(uuid.uuid4())

    audit_record = {
        "record_id": record_id,
        "message_id": message_data.get("message_id", "unknown"),
        "processing_timestamp": datetime.now().isoformat(),
        "message_data": message_data.get("data", {}),
        "message_attributes": message_data.get("attributes", {}),
        "processing_result": processing_result,
        "status": processing_result.get("status", "unknown"),
        "collection": collection_name,
    }

    if "publish_time" in message_data:
        audit_record["original_publish_time"] = message_data["publish_time"]

    doc_ref = db.collection(collection_name).document(record_id)
    doc_ref.set(audit_record)

    return {
        "record_id": record_id,
        "firestore_path": doc_ref.path,
        "collection": collection_name,
        "stored_at": audit_record["processing_timestamp"],
    }


def get_message_audit_record(record_id, collection_name="message_audit"):
    """Retrieve a message audit record from Google Cloud Firestore."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    db = firestore.Client(project=project_id)

    doc_ref = db.collection(collection_name).document(record_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None


def query_message_audit_records(
    message_id=None,
    status=None,
    start_date=None,
    end_date=None,
    collection_name="message_audit",
    limit=100,
):
    """Query message audit records from Google Cloud Firestore."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    db = firestore.Client(project=project_id)

    query = db.collection(collection_name)

    if message_id:
        query = query.where("message_id", "==", message_id)

    if status:
        query = query.where("status", "==", status)

    if start_date:
        query = query.where("processing_timestamp", ">=", start_date.isoformat())

    if end_date:
        query = query.where("processing_timestamp", "<=", end_date.isoformat())

    query = query.limit(limit)

    results = []
    docs = query.stream()

    for doc in docs:
        record = doc.to_dict()
        record["firestore_id"] = doc.id
        results.append(record)

    return results
