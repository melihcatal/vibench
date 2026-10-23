import os
from datetime import datetime
from identity_models import AuditRecord
from managed_store import FirestoreDocumentStore


def store_login_audit(record: AuditRecord, store: FirestoreDocumentStore = None):
    """Persist a federated‑login audit event to a managed NoSQL document store.

    Default store is Google Firestore if no store is supplied.
    The document ID is a composite of user_id and event timestamp for easy lookup.
    """
    if store is None:
        # Configure Firestore using env vars (GOOGLE_APPLICATION_CREDENTIALS implied)
        store = FirestoreDocumentStore(
            project_id=os.getenv("GOOGLE_PROJECT_ID"), collection="login_audit"
        )
    # Build a deterministic document ID: user_id + yyyyMMddHHmmss
    ts_str = datetime.utcfromtimestamp(record.timestamp / 1000).strftime("%Y%m%d%H%M%S")
    doc_id = f"{record.user_id}_{ts_str}"
    store.create_document(doc_id, record.dict())
    return {"document_id": doc_id, "collection": store.collection, "success": True}


# Example usage
# audit = AuditRecord(user_id='12345', event_type='login', timestamp=int(datetime.utcnow().timestamp()*1000), details={})
# result = store_login_audit(audit)
# print(result['document_id'])
