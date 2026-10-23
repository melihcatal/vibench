import os
from google.cloud import firestore

def store_profile_note(user_id: str, note_content: str, metadata: dict = None) -> dict:
    # Google Cloud Firestore requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # or run in a GCP environment with appropriate permissions.
    # The client will automatically pick up credentials from the environment.
    db = firestore.Client()

    notes_collection = db.collection("profile_notes")
    doc_ref = notes_collection.document()

    note_data = {
        "user_id": user_id,
        "note_content": note_content,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "metadata": metadata if metadata is not None else {}
    }

    doc_ref.set(note_data)

    return {"id": doc_ref.id, "message": "Note stored successfully."}

def get_profile_notes(user_id: str) -> list[dict]:
    db = firestore.Client()
    notes_collection = db.collection("profile_notes")

    query = notes_collection.where("user_id", "==", user_id).order_by("timestamp", direction=firestore.Query.DESCENDING)
    results = query.stream()

    notes = []
    for doc in results:
        note = doc.to_dict()
        note["id"] = doc.id
        notes.append(note)
    return notes
