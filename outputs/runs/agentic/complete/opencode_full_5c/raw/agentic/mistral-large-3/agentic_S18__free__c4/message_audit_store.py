from typing import Dict, Any, Optional
from google.cloud import firestore
import os
import json

# Provider-specific: Google Cloud Firestore
# Model/Service: firestore.Client
# Environment variable: GOOGLE_APPLICATION_CREDENTIALS


class MessageAuditStore:
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)

    def store_message(
        self, message_id: str, message_data: Dict[str, Any], status: str
    ) -> None:
        doc_ref = self.db.collection("processed_messages").document(message_id)
        doc_ref.set(
            {
                "message_data": message_data,
                "status": status,
                "timestamp": firestore.SERVER_TIMESTAMP,
            }
        )

    def get_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        doc_ref = self.db.collection("processed_messages").document(message_id)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None
