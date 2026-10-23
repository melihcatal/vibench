import os
from pymongo import MongoClient
from identity_models import ProfileNote, StoreNoteResponse


def store_profile_note(note: ProfileNote) -> StoreNoteResponse:
    connection_string = os.environ.get("MONGO_ATLAS_CONNECTION_STRING")
    client = MongoClient(connection_string)

    try:
        db = client.get_database("onboarding_db")
        notes_collection = db.get_collection("profile_notes")

        result = notes_collection.insert_one(note.dict())

        return StoreNoteResponse(success=True, document_id=str(result.inserted_id))
    except Exception as e:
        return StoreNoteResponse(success=False)
    finally:
        client.close()
