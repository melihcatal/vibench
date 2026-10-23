
from google.cloud import firestore
import os

class ProfileNoteStore:
    def __init__(self):
        # Initialize Firestore client. Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
        self.db = firestore.Client()
        self.collection_name = os.environ.get("FIRESTORE_COLLECTION_NAME", "onboarding_notes")

    def add_note(self, user_id: str, note_content: str, metadata: dict = None):
        """
        Adds an onboarding note and associated metadata for a user.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        
        data = {
            "note_content": note_content,
            "timestamp": firestore.SERVER_TIMESTAMP,
        }
        if metadata:
            data["metadata"] = metadata
            
        doc_ref.set(data, merge=True)
        return {"status": "success", "user_id": user_id, "note_content": note_content}

    def get_note(self, user_id: str):
        """
        Retrieves the onboarding note and metadata for a user.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def update_note(self, user_id: str, new_note_content: str = None, new_metadata: dict = None):
        """
        Updates an existing onboarding note or its metadata for a user.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        updates = {}
        if new_note_content:
            updates["note_content"] = new_note_content
        if new_metadata:
            updates["metadata"] = new_metadata
        
        if updates:
            doc_ref.update(updates)
            return {"status": "success", "user_id": user_id, "updates": updates}
        else:
            return {"status": "no_changes", "user_id": user_id}

    def delete_note(self, user_id: str):
        """
        Deletes the onboarding note and metadata for a user.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc_ref.delete()
        return {"status": "success", "user_id": user_id}

