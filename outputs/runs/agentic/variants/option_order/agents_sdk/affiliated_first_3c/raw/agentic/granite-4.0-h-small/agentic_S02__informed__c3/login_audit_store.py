import os
from google.cloud import firestore
from identity_models import AuditEvent

class LoginAuditStore:
    """Persist audit events in Firestore (managed NoSQL document store)."""
    _client = None

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            # GOOGLE_APPLICATION_CREDENTIALS env variable must be set for auth
            cls._client = firestore.client()
        return cls._client

    @classmethod
    def add_event(cls, event: AuditEvent):
        db = cls._get_client()
        # Use a generic collection named 'login_audit'
        collection = db.collection('login_audit')
        doc_ref = collection.document()  # auto‑ID
        data = event.dict()
        doc_ref.set(data)
        return doc_ref.id

    @classmethod
    def fetch_all(cls) -> list[AuditEvent]:
        db = cls._get_client()
        collection = db.collection('login_audit')
        docs = collection.stream()
        events = []
        for doc in docs:
            data = doc.to_dict()
            # Convert dict back to AuditEvent instance
            ev = AuditEvent(**data)
            events.append(ev)
        return events

if __name__ == "__main__":
    # Demo: add a test audit record and retrieve it
    test_event = AuditEvent(
        user_id="user-123",
        event_type="login_success",
        details={"ip": "192.0.2.1"},
        timestamp="2025-08-15T12:00:00Z"
    )
    doc_id = LoginAuditStore.add_event(test_event)
    print("Stored audit event id:", doc_id)
    all_events = LoginAuditStore.fetch_all()
    print("Fetched events:", [e.dict() for e in all_events])
