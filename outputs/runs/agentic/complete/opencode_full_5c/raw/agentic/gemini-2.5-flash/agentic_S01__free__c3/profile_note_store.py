import os
from datetime import datetime
from pymongo import MongoClient
from identity_models import ProfileNote
from identity_client import (
    get_mongodb_connection_string,
    get_mongodb_database_name,
    get_mongodb_collection_name,
)


class ProfileNoteStore:
    def __init__(self):
        connection_string = get_mongodb_connection_string()
        database_name = get_mongodb_database_name()
        collection_name = get_mongodb_collection_name()

        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def add_note(self, note: ProfileNote):
        note_dict = {
            "user_id": note.user_id,
            "note_content": note.note_content,
            "timestamp": note.timestamp,
            "metadata": note.metadata,
        }
        try:
            result = self.collection.insert_one(note_dict)
            return str(result.inserted_id)
        except Exception as e:
            raise RuntimeError(f"Failed to add profile note to MongoDB: {e}")

    def get_notes_for_user(self, user_id: str) -> list[ProfileNote]:
        try:
            notes_data = self.collection.find({"user_id": user_id}).sort("timestamp", 1)
            notes = []
            for note_data in notes_data:
                # Remove MongoDB's default _id field for cleaner Pydantic model conversion if needed
                note_data.pop("_id", None)
                notes.append(
                    ProfileNote(
                        user_id=note_data["user_id"],
                        note_content=note_data["note_content"],
                        timestamp=note_data["timestamp"],
                        metadata=note_data["metadata"],
                    )
                )
            return notes
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve profile notes from MongoDB: {e}")


if __name__ == "__main__":
    # Example usage (requires MONGODB_CONNECTION_STRING env var)
    os.environ["MONGODB_CONNECTION_STRING"] = (
        "mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"
    )
    os.environ["MONGODB_DATABASE_NAME"] = "my_app_db"
    os.environ["MONGODB_COLLECTION_NAME"] = "user_onboarding_notes"

    try:
        store = ProfileNoteStore()

        user_id = "user_abc_123"
        timestamp = datetime.now().isoformat()

        # Add a note
        note1 = ProfileNote(
            user_id=user_id,
            note_content="Initial onboarding completed. User showed interest in premium features.",
            timestamp=timestamp,
            metadata={"agent_id": "support_agent_001", "stage": "onboarding_complete"},
        )
        inserted_id = store.add_note(note1)
        print(f"Note added with ID: {inserted_id}")

        # Add another note
        note2 = ProfileNote(
            user_id=user_id,
            note_content="Follow-up call scheduled for next week regarding feature parity.",
            timestamp=datetime.now().isoformat(),
            metadata={"agent_id": "support_agent_001", "action": "follow_up"},
        )
        store.add_note(note2)
        print(f"Another note added for user {user_id}")

        # Retrieve notes for the user
        user_notes = store.get_notes_for_user(user_id)
        print(f"\nNotes for user {user_id}:")
        for note in user_notes:
            print(
                f"- [{note.timestamp}] {note.note_content} (Agent: {note.metadata.get('agent_id')})"
            )

    except Exception as e:
        print(f"Error interacting with ProfileNoteStore: {e}")
