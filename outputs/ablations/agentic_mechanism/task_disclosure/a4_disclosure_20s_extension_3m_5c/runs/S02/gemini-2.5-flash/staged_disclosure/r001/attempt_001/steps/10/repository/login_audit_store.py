
from google.cloud import firestore

class LoginAuditStore:
    def __init__(self):
        # Initialize Google Cloud Firestore client
        self.db = firestore.Client()
        self.collection_name = 'federated_login_audits'

    def persist_audit_record(self, record: dict):
        """
        Persists a federated-login audit record to Firestore.
        """
        try:
            doc_ref = self.db.collection(self.collection_name).add(record)
            print(f"Audit record added with ID: {doc_ref[1].id}")
        except Exception as e:
            print(f"Error persisting audit record: {e}")

if __name__ == '__main__':
    # Example Usage:
    audit_store = LoginAuditStore()

    # Simulate a federated login audit record
    audit_record = {
        'timestamp': firestore.SERVER_TIMESTAMP,
        'user_id': 'user123',
        'provider': 'Google',
        'status': 'success',
        'ip_address': '192.168.1.1',
        'details': 'User successfully logged in via Google'
    }

    audit_store.persist_audit_record(audit_record)

    audit_record_2 = {
        'timestamp': firestore.SERVER_TIMESTAMP,
        'user_id': 'user456',
        'provider': 'Okta',
        'status': 'failure',
        'ip_address': '10.0.0.5',
        'error_message': 'MFA required but not provided'
    }
    audit_store.persist_audit_record(audit_record_2)
