import os
from google.cloud import firestore

# Google Firestore configuration from environment variables
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize Firestore client
db = firestore.Client()


class ProfileNoteStore:
    """Persists onboarding notes and support metadata in Google Firestore.

    Provides thread-safe utilities for creating, reading, and updating notes.
    """

    NOTE_COLLECTION = "onboarding_notes"

    @staticmethod
    def store_note(user_id: str, note_id: str, data: dict) -> None:
        """Persist a note into Firestore."""
        doc_ref = db.collection(ProfileNoteStore.NOTE_COLLECTION).document(user_id)
        # Use subcollection 'notes' to group per user
        note_ref = doc_ref.collection("notes").document(note_id)
        note_ref.set(data)

    @staticmethod
    def get_note(user_id: str, note_id: str) -> dict:
        """Retrieve a note from Firestore."""
        doc_ref = db.collection(ProfileNoteStore.NOTE_COLLECTION).document(user_id)
        note_ref = doc_ref.collection("notes").document(note_id)
        doc = note_ref.get()
        return doc.to_dict() if doc.exists else {}

    @staticmethod
    def update_note(user_id: str, note_id: str, updates: dict) -> None:
        """Update an existing note."""
        doc_ref = db.collection(ProfileNoteStore.NOTE_COLLECTION).document(user_id)
        note_ref = doc_ref.collection("notes").document(note_id)
        note_ref.update(updates)
