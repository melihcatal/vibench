
from google.cloud import firestore
import os

class ProfileNoteStore:
    def __init__(self):
        # Initialize Firestore client
        # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        # or that you are running in a Google Cloud environment
        self.db = firestore.Client()
        self.collection_ref = self.db.collection('onboarding_notes')

    def add_note(self, user_id: str, note_content: str, metadata: dict = None):
        """Adds an onboarding note for a user."""
        doc_ref = self.collection_ref.document(user_id)
        data = {
            'note_content': note_content,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'metadata': metadata if metadata is not None else {}
        }
        doc_ref.set(data, merge=True)
        return doc_ref.id

    def get_note(self, user_id: str):
        """Retrieves an onboarding note for a user."""
        doc_ref = self.collection_ref.document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def update_note(self, user_id: str, new_note_content: str, new_metadata: dict = None):
        """Updates an existing onboarding note for a user."""
        doc_ref = self.collection_ref.document(user_id)
        updates = {'note_content': new_note_content, 'timestamp': firestore.SERVER_TIMESTAMP}
        if new_metadata is not None:
            updates['metadata'] = new_metadata
        doc_ref.update(updates)
        return True

    def delete_note(self, user_id: str):
        """Deletes an onboarding note for a user."""
        doc_ref = self.collection_ref.document(user_id)
        doc_ref.delete()
        return True
