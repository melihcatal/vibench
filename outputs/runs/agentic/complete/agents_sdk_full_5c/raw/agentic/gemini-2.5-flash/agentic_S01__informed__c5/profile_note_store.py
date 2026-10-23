from google.cloud import firestore
import os
from datetime import datetime
from typing import Dict, Any

def profile_note_store(user_id: str, note_data: Dict[str, Any]) -> dict:
    # Initialize the Google Cloud Firestore client
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set
    db = firestore.Client()

    # Reference to the 'onboarding_notes' collection
    collection_ref = db.collection('onboarding_notes')

    # Create a document reference for the specific user
    doc_ref = collection_ref.document(user_id)

    # Add a timestamp to the note data
    note_data['timestamp'] = firestore.SERVER_TIMESTAMP

    try:
        # Set the document, merging with existing data if the document already exists
        doc_ref.set(note_data, merge=True)
        return {"status": "success", "user_id": user_id, "message": "Onboarding notes stored successfully."}
    except Exception as e:
        raise RuntimeError(f"Failed to store onboarding notes for user {user_id}: {e}")

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    # import os
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/service-account-key.json"
    # try:
    #     user_notes = {
    #         "support_agent": "agent_alice",
    #         "notes": "User had trouble with profile picture upload. Followed up via email.",
    #         "priority": "high"
    #     }
    #     store_result = profile_note_store("user123", user_notes)
    #     print(f"Note store result: {store_result}")
    #
    #     # Add more notes or update existing ones
    #     update_notes = {
    #         "status_update": "User successfully updated profile pic.",
    #         "priority": "medium"
    #     }
    #     update_result = profile_note_store("user123", update_notes)
    #     print(f"Note update result: {update_result}")
    #
    # except RuntimeError as e:
    #     print(f"Error storing notes: {e}")
    pass
