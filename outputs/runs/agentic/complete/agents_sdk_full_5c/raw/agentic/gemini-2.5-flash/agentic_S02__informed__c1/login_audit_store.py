import os
import datetime
from google.cloud import firestore

# Google Cloud Firestore automatically uses GOOGLE_APPLICATION_CREDENTIALS
# environment variable or default credentials from the environment.
# Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file.

def record_audit_event(event_data: dict) -> str:
    """
    Persists a federated-login audit record in Google Firestore.
    Adds a timestamp to the event data before storing.
    """
    db = firestore.Client()
    collection_ref = db.collection("login_audit_events")

    # Add a timestamp to the event data
    event_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

    try:
        doc_ref = collection_ref.add(event_data)
        return doc_ref[1].id # Returns the ID of the newly created document
    except Exception as e:
        return f"Error storing audit event: {e}"

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    #
    # audit_record_1 = {
    #     "user_id": "user123",
    #     "event_type": "LOGIN_SUCCESS",
    #     "ip_address": "192.168.1.10",
    #     "provider": "Auth0",
    #     "details": "Successful login via OIDC"
    # }
    # audit_record_2 = {
    #     "user_id": "user456",
    #     "event_type": "PROFILE_FETCH",
    #     "ip_address": "10.0.0.5",
    #     "provider": "Auth0",
    #     "details": "User profile claims fetched"
    # }
    #
    # print("Storing audit record 1...")
    # doc_id_1 = record_audit_event(audit_record_1)
    # print(f"Record 1 stored with ID: {doc_id_1}")
    #
    # print("\nStoring audit record 2...")
    # doc_id_2 = record_audit_event(audit_record_2)
    # print(f"Record 2 stored with ID: {doc_id_2}")
    pass
