import os
import json
from typing import Dict, Any

# Placeholder for persisting audit records in a managed NoSQL document store
# This example uses Google Firestore for demonstration
# Production would use google-cloud-firestore SDK or Cosmos DB SDK

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Minimal wrapper around Firestore client (simplified for illustration)
# In practice import google.cloud.firestore as firestore

_firebase_client = None

def _get_firestore_client() -> Any:
    global _firebase_client
    if _firebase_client is None:
        # Import inside function to defer credential load
        from google.cloud import firestore
        _firebase_client = firestore.Client()
    return _firebase_client


def store_audit_record(record: Dict[str, Any]):
    """Persist a federated login audit record."""
    db = _get_firestore_client()
    # Example collection name
    collection = db.collection('federated_login_audit')
    doc_ref = collection.document()  # auto-id
    doc_ref.set(record)
    print(f'Audit record stored with ID: {doc_ref.id}')


def retrieve_recent_audit(limit: int = 10):
    """Fetch the most recent audit records."""
    db = _get_firestore_client()
    collection = db.collection('federated_login_audit')
    docs = collection.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
    results = [doc.to_dict() for doc in docs]
    return results

if __name__ == '__main__':
    sample_audit = {
        'user_id': 'demo_user_123',
        'timestamp': '2025-08-15T13:45:00Z',
        'provider': 'Google Identity Platform',
        'status': 'success',
        'method': 'OIDC'
    }
    store_audit_record(sample_audit)
    recent = retrieve_recent_audit(limit=5)
    print('Recent audits:', json.dumps(recent, indent=2))
