import os
import json
from google.cloud import firestore
from typing import Dict, Any

# Using Google Firestore as a managed NoSQL document store
# Environment variables expected: GOOGLE_APPLICATION_CREDENTIALS

db = firestore.Client()

NOTES_COLLECTION = 'onboarding_notes'


def store_note(user_id: str, note: Dict[str, Any]) -> None:
    """Persist onboarding notes and support metadata for a user.","""    doc_ref = db.collection(NOTES_COLLECTION).document(user_id)
    # Merge with existing document if it exists
    doc_ref.set(note, merge=True)
    print(f"Stored note for {user_id}")


def retrieve_notes(user_id: str) -> Dict[str, Any]:
    """Fetch all notes stored for a user.","""    doc_ref = db.collection(NOTES_COLLECTION).document(user_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise ValueError(f"No notes found for user {user_id}")
    return doc.to_dict()

# Example usage helper
def example_notes_workflow():
    user = 'user-abcde'
    note_payload = {
        'timestamp': '2025-08-14T13:00:00Z',
        'operator': 'support-agent',
        'message': 'User requested password reset assistance.',
        'metadata': {'request_id': 'req-987', 'channel': 'chat'}
    }
    store_note(user, note_payload)
    notes = retrieve_notes(user)
    print(json.dumps(notes, indent=2))
