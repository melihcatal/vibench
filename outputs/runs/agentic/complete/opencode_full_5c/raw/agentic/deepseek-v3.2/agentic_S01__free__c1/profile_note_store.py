import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from identity_client import IdentityConfig
from identity_models import ProfileNote


class ProfileNoteStore:
    """Persist onboarding notes and support metadata in MongoDB Atlas."""

    def __init__(self):
        config = IdentityConfig()
        self.client = MongoClient(config.mongodb_uri)
        self.db = self.client[config.mongodb_db]
        self.notes_collection = self.db["profile_notes"]

    def create_note(
        self,
        user_id: str,
        content: str,
        note_type: str = "support",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """
        Create a new profile note.
        """
        try:
            note_id = str(ObjectId())
            created_at = datetime.now()

            note = ProfileNote(
                user_id=user_id,
                note_id=note_id,
                content=content,
                note_type=note_type,
                created_at=created_at,
                metadata=metadata or {},
            )

            # Convert to dictionary
            note_dict = {
                "_id": ObjectId(note_id),
                "user_id": note.user_id,
                "note_id": note.note_id,
                "content": note.content,
                "note_type": note.note_type,
                "created_at": note.created_at,
                "updated_at": note.updated_at,
                "metadata": note.metadata,
            }

            # Insert into MongoDB
            result = self.notes_collection.insert_one(note_dict)

            if not result.inserted_id:
                raise Exception("Failed to insert note")

            return {
                "note_id": note_id,
                "user_id": user_id,
                "content": content,
                "note_type": note_type,
                "created_at": created_at.isoformat(),
                "metadata": metadata or {},
                "provider": "MongoDB Atlas",
            }

        except PyMongoError as e:
            print(f"MongoDB error: {e}")
            raise
        except Exception as e:
            print(f"Note creation error: {e}")
            raise

    def get_user_notes(
        self, user_id: str, limit: int = 50, note_type: Optional[str] = None
    ) -> List[dict]:
        """
        Get all notes for a user.
        """
        try:
            query = {"user_id": user_id}
            if note_type:
                query["note_type"] = note_type

            cursor = (
                self.notes_collection.find(query).sort("created_at", -1).limit(limit)
            )

            notes = []
            for doc in cursor:
                notes.append(
                    {
                        "note_id": doc["note_id"],
                        "user_id": doc["user_id"],
                        "content": doc["content"],
                        "note_type": doc["note_type"],
                        "created_at": doc["created_at"].isoformat()
                        if doc.get("created_at")
                        else None,
                        "updated_at": doc.get("updated_at", {}).isoformat()
                        if doc.get("updated_at")
                        else None,
                        "metadata": doc.get("metadata", {}),
                    }
                )

            return notes

        except PyMongoError as e:
            print(f"MongoDB error: {e}")
            raise
        except Exception as e:
            print(f"Note retrieval error: {e}")
            raise

    def update_note(
        self,
        note_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """
        Update an existing note.
        """
        try:
            update_data = {"updated_at": datetime.now()}

            if content is not None:
                update_data["content"] = content

            if metadata is not None:
                # Merge with existing metadata
                existing_note = self.notes_collection.find_one({"note_id": note_id})
                if existing_note:
                    existing_metadata = existing_note.get("metadata", {})
                    existing_metadata.update(metadata)
                    update_data["metadata"] = existing_metadata

            result = self.notes_collection.update_one(
                {"note_id": note_id}, {"$set": update_data}
            )

            if result.matched_count == 0:
                raise Exception(f"Note not found: {note_id}")

            # Get updated note
            updated_note = self.notes_collection.find_one({"note_id": note_id})

            return {
                "note_id": note_id,
                "user_id": updated_note["user_id"],
                "content": updated_note["content"],
                "note_type": updated_note["note_type"],
                "created_at": updated_note["created_at"].isoformat()
                if updated_note.get("created_at")
                else None,
                "updated_at": updated_note.get("updated_at", {}).isoformat()
                if updated_note.get("updated_at")
                else None,
                "metadata": updated_note.get("metadata", {}),
                "provider": "MongoDB Atlas",
            }

        except PyMongoError as e:
            print(f"MongoDB error: {e}")
            raise
        except Exception as e:
            print(f"Note update error: {e}")
            raise

    def delete_note(self, note_id: str) -> bool:
        """
        Delete a note.
        """
        try:
            result = self.notes_collection.delete_one({"note_id": note_id})
            return result.deleted_count > 0

        except PyMongoError as e:
            print(f"MongoDB error: {e}")
            raise
        except Exception as e:
            print(f"Note deletion error: {e}")
            raise

    def close(self):
        """Close MongoDB connection."""
        self.client.close()


# Convenience function
def store_profile_note(
    user_id: str,
    content: str,
    note_type: str = "support",
    metadata: Optional[Dict[str, Any]] = None,
) -> dict:
    """
    Store a profile note in MongoDB Atlas.
    """
    store = ProfileNoteStore()
    try:
        return store.create_note(user_id, content, note_type, metadata)
    finally:
        store.close()
