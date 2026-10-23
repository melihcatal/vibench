from google.cloud import firestore
import datetime

class ProfileNoteStore:
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)
        self.collection_ref = self.db.collection('onboarding_notes')

    def save_note(self, user_id: str, note_content: str, metadata: dict = None):
        if not user_id or not note_content:
            raise ValueError("User ID and note content cannot be empty.")

        note_data = {
            "user_id": user_id,
            "note_content": note_content,
            "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
        }
        if metadata:
            note_data["metadata"] = metadata

        doc_ref = self.collection_ref.document()
        doc_ref.set(note_data)
        return doc_ref.id

    def get_notes_by_user(self, user_id: str):
        if not user_id:
            raise ValueError("User ID cannot be empty.")
        
        notes = []
        query = self.collection_ref.where('user_id', '==', user_id).stream()
        for doc in query:
            notes.append(doc.to_dict())
        return notes

# Example usage (for demonstration, in a real application, project_id might come from an environment variable)
# if __name__ == "__main__":
#     # Replace 'your-google-cloud-project-id' with your actual Google Cloud Project ID
#     # Ensure your GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
#     # authenticated using `gcloud auth application-default login`
#     project_id = 'your-google-cloud-project-id' 
#     store = ProfileNoteStore(project_id)

#     # Save a note
#     note_id = store.save_note(
#         user_id="user123",
#         note_content="Initial onboarding discussion notes.",
#         metadata={"agent": "support_agent_alpha", "category": "onboarding"}
#     )
#     print(f"Note saved with ID: {note_id}")

#     # Get notes for a user
#     user_notes = store.get_notes_by_user("user123")
#     print(f"Notes for user123: {user_notes}")
