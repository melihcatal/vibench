import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class ProfileNoteStore:
    """Persist onboarding notes and support metadata in MongoDB Atlas."""

    def __init__(self):
        self.connection_string = os.getenv("MONGODB_ATLAS_URI")
        if not self.connection_string:
            raise ValueError("MONGODB_ATLAS_URI environment variable not set")

        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database("onboarding_db")
        self.collection = self.db.get_collection("profile_notes")

    def store_note(
        self,
        user_id: str,
        note_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """
        Store a profile note for a user.
        """
        note_doc = {
            "user_id": user_id,
            "note_type": note_type,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "provider": "mongodb-atlas",
        }

        try:
            result = self.collection.insert_one(note_doc)

            return {
                "note_id": str(result.inserted_id),
                "user_id": user_id,
                "note_type": note_type,
                "created_at": note_doc["created_at"].isoformat(),
                "success": True,
                "provider": "mongodb-atlas",
            }
        except PyMongoError as e:
            raise RuntimeError(f"Failed to store note: {str(e)}")

    def get_user_notes(
        self, user_id: str, note_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all notes for a user, optionally filtered by note type.
        """
        query = {"user_id": user_id}
        if note_type:
            query["note_type"] = note_type

        try:
            notes = list(self.collection.find(query).sort("created_at", -1))

            result = []
            for note in notes:
                note["_id"] = str(note["_id"])
                if isinstance(note.get("created_at"), datetime):
                    note["created_at"] = note["created_at"].isoformat()
                if isinstance(note.get("updated_at"), datetime):
                    note["updated_at"] = note["updated_at"].isoformat()
                result.append(note)

            return result
        except PyMongoError as e:
            raise RuntimeError(f"Failed to retrieve notes: {str(e)}")

    def update_note(
        self, note_id: str, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> dict:
        """
        Update an existing note.
        """
        try:
            update_data = {"content": content, "updated_at": datetime.utcnow()}

            if metadata is not None:
                update_data["metadata"] = metadata

            result = self.collection.update_one({"_id": note_id}, {"$set": update_data})

            if result.matched_count == 0:
                raise ValueError(f"Note with ID {note_id} not found")

            return {
                "note_id": note_id,
                "updated": True,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "provider": "mongodb-atlas",
            }
        except PyMongoError as e:
            raise RuntimeError(f"Failed to update note: {str(e)}")

    def delete_note(self, note_id: str) -> dict:
        """
        Delete a note by ID.
        """
        try:
            result = self.collection.delete_one({"_id": note_id})

            if result.deleted_count == 0:
                raise ValueError(f"Note with ID {note_id} not found")

            return {
                "note_id": note_id,
                "deleted": True,
                "deleted_count": result.deleted_count,
                "provider": "mongodb-atlas",
            }
        except PyMongoError as e:
            raise RuntimeError(f"Failed to delete note: {str(e)}")

    def store_support_metadata(
        self, user_id: str, support_case_id: str, metadata: Dict[str, Any]
    ) -> dict:
        """
        Store support metadata for a user.
        """
        return self.store_note(
            user_id=user_id,
            note_type="support_metadata",
            content=f"Support case: {support_case_id}",
            metadata=metadata,
        )

    def store_onboarding_progress(
        self,
        user_id: str,
        step_name: str,
        status: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """
        Store onboarding progress tracking.
        """
        metadata = {"step_name": step_name, "status": status, "details": details or {}}

        return self.store_note(
            user_id=user_id,
            note_type="onboarding_progress",
            content=f"Onboarding step '{step_name}' status: {status}",
            metadata=metadata,
        )

    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
