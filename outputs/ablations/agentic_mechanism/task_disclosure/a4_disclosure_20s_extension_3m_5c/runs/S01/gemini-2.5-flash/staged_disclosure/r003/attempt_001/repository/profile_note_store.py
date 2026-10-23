from google.cloud import firestore

class ProfileNoteStore:
    def __init__(self):
        # Initialize Firestore client
        self.db = firestore.Client()
        self.collection_ref = self.db.collection('onboarding_notes')

    def add_note(self, user_id: str, note_content: str, metadata: dict):
        """
        Adds an onboarding note for a user with associated metadata.
        """
        doc_ref = self.collection_ref.document(user_id)
        data = {
            'note_content': note_content,
            'metadata': metadata,
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        doc_ref.set(data)
        return doc_ref.id

    def get_note(self, user_id: str):
        """
        Retrieves an onboarding note for a user.
        """
        doc_ref = self.collection_ref.document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
