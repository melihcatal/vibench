# [LATER-STEP] profile_note_store.py
from identity_models import NoteStoreRequest, NoteStoreResponse
from typing import Dict, Any

# Placeholder for a managed document store SDK, e.g., AWS DynamoDB, Firestore, etc.
# from google.cloud import firestore

# In-memory mock for this template (replace with real client)
notes_db: Dict[str, Dict[str, Any]] = {}


def store_onboarding_note(request: NoteStoreRequest) -> NoteStoreResponse:
    note_id = request.note_id if request.note_id else str(len(notes_db) + 1)
    # Simple JSON-like persistence in the in-memory dict
    notes_db[note_id] = {"content": request.content, "metadata": request.metadata or {}}
    return NoteStoreResponse(note_id=note_id, stored=True)
