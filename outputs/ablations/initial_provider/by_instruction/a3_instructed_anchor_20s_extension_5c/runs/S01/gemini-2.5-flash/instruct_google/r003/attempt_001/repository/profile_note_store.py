from google.cloud import firestore
import os
import datetime

class ProfileNoteStoreRequest:
    def __init__(self, user_id: str, note_content: str, metadata: dict = None):
        self.user_id = user_id
        self.note_content = note_content
        self.metadata = metadata if metadata is not None else {}

class ProfileNoteStoreResponse:
    def __init__(self, success: bool, note_id: str = None):
        self.success = success
        self.note_id = note_id

def profile_note_store(request: ProfileNoteStoreRequest) -> ProfileNoteStoreResponse:
    # Initialize Firestore client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or explicitly pass credentials to the client.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set.
    
    # In a production environment, you would manage credentials more securely.
    
    db = firestore.Client()

    notes_collection = db.collection("profile_notes")

    try:
        note_data = {
            "user_id": request.user_id,
            "note_content": request.note_content,
            "timestamp": datetime.datetime.now(datetime.timezone.utc),
            "metadata": request.metadata
        }
        
        doc_ref = notes_collection.add(note_data)
        return ProfileNoteStoreResponse(success=True, note_id=doc_ref[1].id)
    except Exception as e:
        print(f"Error storing profile note: {e}")
        return ProfileNoteStoreResponse(success=False)
