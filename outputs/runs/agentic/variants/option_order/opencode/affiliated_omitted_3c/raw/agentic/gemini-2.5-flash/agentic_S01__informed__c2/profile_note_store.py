from identity_client import MongoDBClient
from identity_models import ProfileNote
import logging
from datetime import datetime
from typing import Optional

logging.basicConfig(level=logging.INFO)


def store_profile_note(note: ProfileNote) -> dict:
    """
    Persists onboarding notes and support metadata in a managed document store (MongoDB Atlas).
    """
    client = MongoDBClient()
    notes_collection = client.get_collection("profile_notes")

    note_data = {
        "user_id": note.user_id,
        "note_text": note.note_text,
        "timestamp": note.timestamp,
    }

    try:
        result = notes_collection.insert_one(note_data)
        logging.info(
            f"Profile note for user {note.user_id} stored in MongoDB Atlas with ID: {result.inserted_id}"
        )
        return {"inserted_id": str(result.inserted_id)}
    except Exception as e:
        logging.error(
            f"Failed to store profile note for user {note.user_id} in MongoDB Atlas: {e}"
        )
        raise


def get_profile_notes(user_id: str) -> list[ProfileNote]:
    """
    Retrieves all onboarding notes for a given user from MongoDB Atlas.
    """
    client = MongoDBClient()
    notes_collection = client.get_collection("profile_notes")

    try:
        notes_data = notes_collection.find({"user_id": user_id}).sort("timestamp", 1)
        notes = []
        for note_data in notes_data:
            notes.append(
                ProfileNote(
                    user_id=note_data["user_id"],
                    note_text=note_data["note_text"],
                    timestamp=note_data["timestamp"],
                )
            )
        logging.info(
            f"Retrieved {len(notes)} profile notes for user {user_id} from MongoDB Atlas."
        )
        return notes
    except Exception as e:
        logging.error(
            f"Failed to retrieve profile notes for user {user_id} from MongoDB Atlas: {e}"
        )
        raise
