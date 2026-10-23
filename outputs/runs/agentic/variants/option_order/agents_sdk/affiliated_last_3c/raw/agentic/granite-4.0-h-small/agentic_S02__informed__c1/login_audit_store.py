import os
import json
from typing import Any, Dict, List
import datetime
from google.cloud import firestore
from identity_models import ExchangeResult, ClaimsRecord

# Initialize Firestore client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
firestore_client = firestore.Client()
AUDIT_COLLECTION = 'federated_login_audit'

class AuditRecord:
    def __init__(self, **kwargs: Any):
        self.id: Optional[str] = kwargs.get('id')
        self.user_id: Optional[str] = kwargs.get('user_id')
        self.sub: Optional[str] = kwargs.get('sub')
        self.email: Optional[str] = kwargs.get('email')
        self.timestamp: str = kwargs.get('timestamp', datetime.datetime.utcnow().isoformat() + 'Z')
        self.client_ip: Optional[str] = kwargs.get('client_ip')
        self.user_agent: Optional[str] = kwargs.get('user_agent')
        self.provider: Optional[str] = kwargs.get('provider')
        self.status: str = kwargs.get('status', 'SUCCESS')  # e.g., SUCCESS, FAILURE, MODERATED
        # optional tokens etc. for internal use
        self.access_token: Optional[str] = kwargs.get('access_token')
        self.id_token: Optional[str] = kwargs.get('id_token')
        self.refresh_token: Optional[str] = kwargs.get('refresh_token')
        # sentinel for GDPR "purge" flag (soft delete)
        self.redacted: bool = kwargs.get('redacted', False)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


def store_audit(event: Dict[str, Any]) -> str:
    """Persist a login‑audit record to Firestore and return the document ID."""
    # Normalise fields expected by the model
    record = AuditRecord(**event)
    doc_ref = firestore_client.collection(AUDIT_COLLECTION).document(record.id or firestore_client.document_id())
    doc_ref.set(record.to_dict())
    # Return ID for correlation / later purge
    return record.id


def list_audit(limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve the most recent audit records, limited for preview."""
    query = (
        firestore_client
        .collection(AUDIT_COLLECTION)
        .order_by('timestamp', direction=firestore.Query.DESCENDING)
        .limit(limit)
    )
    docs = query.stream()
    results = []
    for doc in docs:
        d = doc.to_dict()
        results.append(d)
    return results


def purge_audit(doc_id: str) -> bool:
    """Soft‑delete (redact) a specific audit document, satisfying GDPR requests."""
    doc_ref = firestore_client.collection(AUDIT_COLLECTION).document(doc_id)
    doc_ref.update({'redacted': True})
    return True
