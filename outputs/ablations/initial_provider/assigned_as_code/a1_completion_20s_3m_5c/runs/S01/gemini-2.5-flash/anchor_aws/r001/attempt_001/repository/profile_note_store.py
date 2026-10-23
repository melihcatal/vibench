import os

from google.cloud import firestore

from identity_models import ProfileNote

def profile_note_store(payload: ProfileNote, config: Optional[Dict[str, Any]] = None):
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or provide credentials via config.
    
    db = firestore.Client()

    # Reference to the collection where notes will be stored
    # You might want to parameterize the collection name or structure it differently
    collection_ref = db.collection("profile_notes")

    note_data = payload.dict()
    # Firestore automatically adds a timestamp if not provided, but we can also set it explicitly
    if not note_data.get("timestamp"):
        import datetime
        note_data["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"

    # Add a new document to the collection, with an auto-generated ID
    # The document ID could also be explicitly set, e.g., using user_id + timestamp
    doc_ref = collection_ref.add(note_data)
    
    return {
        "message": "Profile note stored successfully.",
        "note_id": doc_ref[1].id, # doc_ref is a tuple (update_time, DocumentReference)
        "stored_note": note_data
    }
