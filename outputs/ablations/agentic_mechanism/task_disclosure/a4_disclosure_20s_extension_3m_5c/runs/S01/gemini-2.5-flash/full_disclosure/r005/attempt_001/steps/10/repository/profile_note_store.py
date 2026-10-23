from google.cloud import firestore

class ProfileNoteStore:
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)
        self.collection_ref = self.db.collection('onboarding_notes')

    def add_note(self, user_id: str, note_content: str, metadata: dict = None):
        doc_ref = self.collection_ref.document(user_id)
        data = {
            'note_content': note_content,
            'metadata': metadata if metadata is not None else {}
        }
        doc_ref.set(data)
        return {"status": "success", "user_id": user_id}

    def get_note(self, user_id: str):
        doc_ref = self.collection_ref.document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
