import os
import datetime
from google.cloud import firestore  # GOOGLE-specific
from identity_models import UserProfileClaims


class LoginAuditStore:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
        self.db = firestore.Client()  # GOOGLE-specific
        self.collection_name = "login_audits"

    def persist_audit_record(self, user_id: str, action: str, details: dict):
        doc_ref = self.db.collection(self.collection_name).document()
        record = {
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
            "details": details,
        }
        doc_ref.set(record)
        return doc_ref.id

    def get_audit_records(self, user_id: str = None, limit: int = 10):
        query = self.db.collection(self.collection_name).order_by(
            "timestamp", direction=firestore.Query.DESCENDING
        )  # GOOGLE-specific
        if user_id:
            query = query.where("user_id", "==", user_id)  # GOOGLE-specific
        docs = query.limit(limit).stream()  # GOOGLE-specific
        return [doc.to_dict() for doc in docs]
