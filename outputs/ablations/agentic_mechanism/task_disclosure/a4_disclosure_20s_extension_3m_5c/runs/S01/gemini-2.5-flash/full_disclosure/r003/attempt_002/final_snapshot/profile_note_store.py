from google.cloud import firestore
import os

class ProfileNoteStore:
    def __init__(self, project_id: str = None):
        if project_id is None:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        self.db = firestore.Client(project=project_id)
        self.collection_name = "onboarding_notes"

    def add_note(self, user_id: str, note_content: str, metadata: dict = None) -> str:
        doc_ref = self.db.collection(self.collection_name).document()
        data = {
            "user_id": user_id,
            "note_content": note_content,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "metadata": metadata if metadata is not None else {}
        }
        doc_ref.set(data)
        return doc_ref.id

    def get_notes_for_user(self, user_id: str) -> list:
        notes = []
        docs = self.db.collection(self.collection_name).where("user_id", "==", user_id).stream()
        for doc in docs:
            note_data = doc.to_dict()
            note_data["id"] = doc.id
            notes.append(note_data)
        return notes
