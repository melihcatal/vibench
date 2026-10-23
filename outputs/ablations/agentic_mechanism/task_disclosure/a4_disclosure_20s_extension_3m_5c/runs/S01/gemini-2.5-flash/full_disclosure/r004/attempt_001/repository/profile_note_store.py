from google.cloud import firestore
import os

class ProfileNoteStore:
    def __init__(self):
        # Initialize Google Cloud Firestore client
        # This assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        # or running in a GCP environment with appropriate permissions.
        self.db = firestore.Client()
        self.collection_name = os.getenv("FIRESTORE_COLLECTION_NAME", "onboarding_notes")

    def add_note(self, user_id: str, note_content: str, metadata: dict = None):
        """
        Adds an onboarding note for a given user.

        Args:
            user_id: The ID of the user.
            note_content: The content of the onboarding note.
            metadata: Optional dictionary of additional support metadata.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        data = {
            "note_content": note_content,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "metadata": metadata if metadata is not None else {}
        }
        doc_ref.set(data, merge=True)
        return {"status": "success", "user_id": user_id}

    def get_note(self, user_id: str):
        """
        Retrieves the onboarding note and metadata for a given user.

        Args:
            user_id: The ID of the user.

        Returns:
            A dictionary containing the note and metadata, or None if not found.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def update_note(self, user_id: str, note_content: str = None, metadata: dict = None):
        """
        Updates an existing onboarding note or its metadata for a given user.

        Args:
            user_id: The ID of the user.
            note_content: Optional new content for the onboarding note.
            metadata: Optional dictionary of additional support metadata to merge.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        update_data = {}
        if note_content is not None:
            update_data["note_content"] = note_content
        if metadata is not None:
            update_data["metadata"] = metadata

        if update_data:
            doc_ref.update(update_data)
            return {"status": "success", "user_id": user_id}
        else:
            return {"status": "no_changes", "user_id": user_id}

    def delete_note(self, user_id: str):
        """
        Deletes the onboarding note for a given user.

        Args:
            user_id: The ID of the user.
        """
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc_ref.delete()
        return {"status": "success", "user_id": user_id}
