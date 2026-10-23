import os
from google.cloud import firestore

class MessageAuditStore:
    def __init__(self):
        # Google Cloud Firestore client
        self.db = firestore.Client()
        self.collection_name = os.getenv("FIRESTORE_COLLECTION_NAME", "message_audit_records")

    def persist_record(self, message_id: str, payload: dict, status: str, timestamp: str):
        doc_ref = self.db.collection(self.collection_name).document(message_id)
        doc_ref.set({
            "payload": payload,
            "status": status,
            "timestamp": timestamp
        })
        return {"status": "success", "message_id": message_id}

    def get_record(self, message_id: str):
        doc_ref = self.db.collection(self.collection_name).document(message_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
