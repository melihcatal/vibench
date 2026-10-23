from google.cloud import firestore
from datetime import datetime
from typing import Dict, Any

from identity_client import GCP_PROJECT_ID, FIRESTORE_AUDIT_COLLECTION
from identity_models import FederatedLoginEvent, UserProfileClaims

def persist_login_audit_record(event: FederatedLoginEvent) -> str:
    """
    Persists a federated login audit record in Google Cloud Firestore.
    """
    db = firestore.Client(project=GCP_PROJECT_ID)
    doc_ref = db.collection(FIRESTORE_AUDIT_COLLECTION).document(event.event_id)

    event_data = event.to_dict()
    # Ensure timestamp is a datetime object for Firestore
    if isinstance(event_data.get("timestamp"), str):
        event_data["timestamp"] = datetime.fromisoformat(event_data["timestamp"])

    doc_ref.set(event_data)
    
    print(f"Successfully persisted login audit event with ID: {event.event_id}")
    return event.event_id

def get_login_audit_record(event_id: str) -> Optional[FederatedLoginEvent]:
    """
    Retrieves a federated login audit record from Google Cloud Firestore.
    """
    db = firestore.Client(project=GCP_PROJECT_ID)
    doc_ref = db.collection(FIRESTORE_AUDIT_COLLECTION).document(event_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        if data:
            # Reconstruct FederatedLoginEvent from dictionary
            claims_data = data.pop("claims", None)
            claims = UserProfileClaims(**claims_data) if claims_data else None
            
            # Convert timestamp back to datetime if it's a Firestore Timestamp object
            if "timestamp" in data and hasattr(data["timestamp"], "astimezone"):
                data["timestamp"] = data["timestamp"].astimezone(datetime.utc).replace(tzinfo=None)

            return FederatedLoginEvent(claims=claims, **data)
    return None

if __name__ == "__main__":
    # Example Usage
    print(f"Using Firestore collection: {FIRESTORE_AUDIT_COLLECTION} in project: {GCP_PROJECT_ID}")

    # Create a dummy user profile claim
    dummy_claims = UserProfileClaims(
        sub="test_user_123",
        email="test@example.com",
        given_name="Test",
        family_name="User",
        okta_profile_id="oktaid_abc"
    )

    # Create a dummy login event
    dummy_event = FederatedLoginEvent(
        provider="Okta",
        user_id=dummy_claims.sub,
        email=dummy_claims.email,
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        login_successful=True,
        claims=dummy_claims,
        login_type="OAuth2",
        metadata={"session_id": "sess_xyz"}
    )

    try:
        # Persist the event
        persisted_event_id = persist_login_audit_record(dummy_event)
        print(f"Login event persisted with ID: {persisted_event_id}")

        # Retrieve the event
        retrieved_event = get_login_audit_record(persisted_event_id)
        if retrieved_event:
            print("\n--- Retrieved Login Event ---")
            print(retrieved_event.to_dict())
            assert retrieved_event.event_id == dummy_event.event_id
            assert retrieved_event.user_id == dummy_event.user_id
            print("Retrieved event matches original event.")
        else:
            print(f"Failed to retrieve event with ID: {persisted_event_id}")
    except Exception as e:
        print(f"Error during Firestore operations: {e}")
        print("Please ensure your GCP_PROJECT_ID is correct and you have appropriate IAM permissions for Firestore.")
        print("Also, ensure the Firestore database is initialized in your project.")
