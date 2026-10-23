from google.cloud import firestore
import os

class ProfileNoteStore:
    def __init__(self):
        # Initialize Firestore client. Assumes GOOGLE_APPLICATION_CREDENTIALS
        # environment variable is set for authentication, or runs on GCP.
        self.db = firestore.Client()
        self.collection_name = os.getenv("FIRESTORE_COLLECTION_NAME", "onboarding_notes")

    def save_note(self, user_id: str, note_content: str, metadata: dict):
        """
        Saves an onboarding note and associated metadata to Firestore.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        data = {
            "note_content": note_content,
            "metadata": metadata,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        doc_ref.set(data)
        return f"Note for user {user_id} saved successfully in collection {self.collection_name}."

    def get_note(self, user_id: str):
        """
        Retrieves an onboarding note and associated metadata from Firestore.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

