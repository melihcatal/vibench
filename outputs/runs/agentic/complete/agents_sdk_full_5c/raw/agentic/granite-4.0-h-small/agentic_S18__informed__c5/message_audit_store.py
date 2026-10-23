# message_audit_store.py
# LATER-STEP: persist processed Pub/Sub message records in Google Cloud Firestore for later lookup

from google.cloud import firestore
from datetime import datetime
from typing import Dict, Any

# Firestore client wrapper
class AuditStore:
    def __init__(self, project_id: str = None):
        self.db = firestore.Client(project=project_id)
        # Collection name where processed messages will be stored
        self.collection_name = "processed_messages"

    def add(self, message: Dict[str, Any]) -> None:
        """Store a normalized message record with a generated document ID.

        Args:
            message: A dict that conforms to the NormalizedMessage model.
        """
        # Use a deterministic ID based on event_id to avoid duplicates
        doc_id = message.get("event_id") or str(datetime.utcnow().timestamp())
        # Ensure the doc has a timestamp for ordering
        message["_stored_at"] = datetime.utcnow().isoformat() + "Z"
        self.db.collection(self.collection_name).document(doc_id).set(message)
        print(f"Stored message {doc_id} in collection {self.collection_name}")

# Example usage (requires GOOGLE_APPLICATION_CREDENTIALS env var)
# store = AuditStore(project_id="my-gcp-project")
# store.add({"event_type":"order_created","event_id":"ord-123","payload":{},"received_at":datetime.utcnow()})
