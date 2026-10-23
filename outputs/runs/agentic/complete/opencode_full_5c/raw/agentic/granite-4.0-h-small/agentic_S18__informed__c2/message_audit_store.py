from messaging_models import MessageRecord
from pydantic import BaseModel
from google.cloud import firestore
import os

FIRESTORE_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")

# Define a small Firestore document structure


class AuditDocument(BaseModel):
    original: dict
    processed: dict = None
    status: str = "received"
    error: str = None
    created_at: str = None


def store_audit(record: MessageRecord) -> None:
    """Persist a processed MessageRecord to Cloud Firestore.",
    Each record becomes a document under the collection 'message_audit'.
    """
    if not record.error:
        record.status = "processed"
    doc_data = {
        "original": record.original,
        "processed": record.processed,
        "status": record.status,
        "error": record.error,
        "created_at": firestore.SERVER_TIMESTAMP,
    }
    db = firestore.Client(project=FIRESTORE_PROJECT)
    doc_ref = db.collection("message_audit").document(
        record.original.get("message_id") or str(record.original.get("id") or "unknown")
    )
    doc_ref.set(doc_data)
