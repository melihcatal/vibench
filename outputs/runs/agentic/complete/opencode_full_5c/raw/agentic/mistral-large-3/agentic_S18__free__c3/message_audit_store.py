from typing import Dict, Any, Optional
from google.cloud import firestore
import os
import json

# Provider: Google Cloud Firestore
# Model/Service: firestore.Client
# Environment Variable: GOOGLE_APPLICATION_CREDENTIALS


class MessageAuditStore:
    def __init__(self):
        self.client = firestore.Client()
        self.collection = self.client.collection("message_audits")

    def store_message_record(self, message_id: str, record_data: Dict[str, Any]) -> str:
        """
        Persists a processed message record in Google Cloud Firestore.
        Returns the document ID.
        """
        doc_ref = self.collection.document(message_id)
        doc_ref.set(record_data)
        return doc_ref.id

    def get_message_record(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a processed message record from Google Cloud Firestore.
        """
        doc_ref = self.collection.document(message_id)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None
