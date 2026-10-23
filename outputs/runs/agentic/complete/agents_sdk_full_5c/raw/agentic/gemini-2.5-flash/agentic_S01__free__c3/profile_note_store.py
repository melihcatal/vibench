import os
import time
from google.cloud import firestore
from identity_models import StoreProfileNoteRequest, StoreProfileNoteResponse, ProfileNote

# Google Cloud Project ID
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
FIRESTORE_COLLECTION_NAME = "user_onboarding_notes" # Firestore specific collection name

def profile_note_store(request: StoreProfileNoteRequest) -> StoreProfileNoteResponse:
    if not GOOGLE_CLOUD_PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable is not set.")

    db = firestore.Client(project=GOOGLE_CLOUD_PROJECT_ID)

    try:
        # Create a new document reference with an auto-generated ID
        doc_ref = db.collection(FIRESTORE_COLLECTION_NAME).document()
        
        current_timestamp = time.time()
        note_data = {
            "user_id": request.user_id,
            "content": request.content,
            "timestamp": current_timestamp,
            "metadata": request.metadata if request.metadata is not None else {}
        }

        doc_ref.set(note_data)
        
        return StoreProfileNoteResponse(note_id=doc_ref.id, timestamp=current_timestamp)
    except Exception as e:
        raise RuntimeError(f"Failed to store profile note in Firestore: {e}")

if __name__ == '__main__':
    # This block is for demonstration/testing only
    # os.environ["GOOGLE_CLOUD_PROJECT_ID"] = "your-gcp-project-id"
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/gcp-service-account.json"
    # try:
    #     store_req = StoreProfileNoteRequest(
    #         user_id="user123",
    #         content="User expressed interest in premium features during onboarding.",
    #         metadata={"agent_id": "support_agent_001", "priority": "high"}
    #     )
    #     store_res = profile_note_store(store_req)
    #     print(f"Profile note stored. Note ID: {store_res.note_id}, Timestamp: {store_res.timestamp}")

    #     # Example of reading it back (optional, not required by prompt)
    #     # db = firestore.Client(project=os.environ["GOOGLE_CLOUD_PROJECT_ID"])
    #     # retrieved_doc = db.collection(FIRESTORE_COLLECTION_NAME).document(store_res.note_id).get()
    #     # if retrieved_doc.exists:
    #     #     print(f"Retrieved note content: {retrieved_doc.to_dict()['content']}")

    # except RuntimeError as e:
    #     print(f"Note store error: {e}")
    pass
