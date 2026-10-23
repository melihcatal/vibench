import uuid
import datetime
from identity_client import IdentityClient
from identity_models import ProfileNote, StoreNoteResponse

def profile_note_store(note: ProfileNote) -> StoreNoteResponse:
    client = IdentityClient()

    if not client.mongodb_collection:
        raise ValueError("MongoDB Atlas client not configured.")

    try:
        # Add a unique ID and timestamp if not already present
        if not hasattr(note, "note_id") or not note.note_id:
            note.note_id = str(uuid.uuid4())
        if not note.timestamp:
            note.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Convert dataclass to dictionary for MongoDB insertion
        note_dict = {k: v for k, v in note.__dict__.items() if v is not None}

        result = client.mongodb_collection.insert_one(note_dict)

        return StoreNoteResponse(note_id=str(result.inserted_id), message="Profile note stored successfully.")
    except Exception as e:
        raise RuntimeError(f"MongoDB Atlas note storage failed: {e}")
