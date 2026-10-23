import os
import datetime
from google.cloud import firestore
from identity_models import LoginAuditRecord

# Configure Google Firestore
# GOOGLE_APPLICATION_CREDENTIALS should be set in the environment or passed implicitly.


def persist_audit_record(record: LoginAuditRecord) -> dict:
    """
    Persists a federated-login audit record in Google Cloud Firestore.
    Args:
        record: An instance of LoginAuditRecord to persist.
    Returns:
        A dictionary indicating the status of the persistence operation.
    """
    try:
        db = firestore.Client()
        doc_ref = db.collection("login_audit_records").document()
        record_data = record.model_dump()
        record_data["timestamp"] = datetime.datetime.now(
            datetime.timezone.utc
        )  # Store timestamp as datetime object
        doc_ref.set(record_data)
        return {"status": "success", "document_id": doc_ref.id}
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error persisting audit record to Firestore: {e}",
        }


if __name__ == "__main__":
    # Example usage:
    sample_audit_record = LoginAuditRecord(
        user_id="auth0|testuser123",
        event_type="login_success",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        ip_address="203.0.113.45",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        provider="Auth0",
        status="success",
        normalized_profile={
            "sub": "auth0|testuser123",
            "email": "test@example.com",
            "name": "Test User",
        },
    )
    result = persist_audit_record(sample_audit_record)
    print("Persistence Result:")
    print(result)
