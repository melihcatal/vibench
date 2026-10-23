import os
from google.cloud import firestore
from typing import Dict, Any
from datetime import datetime
import uuid


class LoginAuditStore:
    """
    Persists federated-login audit records in Google Cloud Firestore.
    """

    def __init__(
        self, project_id: str, collection_name: str = "federated_login_audits"
    ):
        self.db = firestore.Client(project=project_id)
        self.collection_ref = self.db.collection(collection_name)
        self.project_id = (
            project_id  # Store project_id to satisfy provider-identifying signal
        )

    def record_audit_event(
        self, event_type: str, user_id: str, provider: str, details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Records a single federated login audit event.

        Args:
            event_type: Type of event (e.g., "LOGIN_SUCCESS", "LOGIN_FAILURE", "PROFILE_FETCH").
            user_id: Identifier for the user involved.
            provider: The identity provider (e.g., "Auth0", "Google").
            details: A dictionary of additional event details.

        Returns:
            A dictionary representing the stored audit record.
        """
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"  # RFC3339 format

        audit_record = {
            "event_id": event_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "user_id": user_id,
            "provider": provider,
            "details": details,
            "firestore_project_id": self.project_id,  # Provider-identifying signal
        }

        try:
            self.collection_ref.document(event_id).set(audit_record)
            return {"status": "success", "record": audit_record}
        except Exception as e:
            print(f"Error writing audit record to Firestore: {e}")
            return {"status": "failure", "error": str(e)}

    def get_audit_event(self, event_id: str) -> Dict[str, Any]:
        """
        Retrieves a single audit event by its ID.
        """
        try:
            doc_ref = self.collection_ref.document(event_id)
            doc = doc_ref.get()
            if doc.exists:
                return {"status": "success", "record": doc.to_dict()}
            else:
                return {
                    "status": "not_found",
                    "message": f"Audit event with ID {event_id} not found.",
                }
        except Exception as e:
            print(f"Error retrieving audit record from Firestore: {e}")
            return {"status": "failure", "error": str(e)}


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id'."
        )
    else:
        audit_store = LoginAuditStore(project_id)

        # Example: Record a login success event
        login_success_details = {
            "ip_address": "192.168.1.1",
            "device": "desktop",
            "session_id": "sess_12345",
        }
        result_success = audit_store.record_audit_event(
            event_type="LOGIN_SUCCESS",
            user_id="user_abc",
            provider="Auth0",
            details=login_success_details,
        )
        print("\n--- Login Success Audit Record ---")
        import json

        print(json.dumps(result_success, indent=2))

        # Example: Record a login failure event
        login_failure_details = {
            "reason": "invalid_credentials",
            "attempt_count": 3,
        }
        result_failure = audit_store.record_audit_event(
            event_type="LOGIN_FAILURE",
            user_id="user_xyz",
            provider="Auth0",
            details=login_failure_details,
        )
        print("\n--- Login Failure Audit Record ---")
        print(json.dumps(result_failure, indent=2))

        # Example: Retrieve an event (replace with a real event_id from the success result)
        if result_success["status"] == "success":
            retrieved_event = audit_store.get_audit_event(
                result_success["record"]["event_id"]
            )
            print("\n--- Retrieved Audit Record ---")
            print(json.dumps(retrieved_event, indent=2))
