import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from bson import ObjectId
from identity_models import UserProfile


class ProfileNoteStore:
    """Store onboarding notes and support metadata in MongoDB Atlas."""

    def __init__(self):
        connection_string = os.environ.get("MONGODB_ATLAS_CONNECTION_STRING")
        if not connection_string:
            raise ValueError(
                "MONGODB_ATLAS_CONNECTION_STRING environment variable is required"
            )

        self.client = MongoClient(connection_string)
        self.db = self.client.get_database("user_onboarding")
        self.notes_collection = self.db["profile_notes"]
        self.metadata_collection = self.db["support_metadata"]

    def store_onboarding_note(
        self,
        user_id: str,
        note_type: str,
        content: str,
        metadata: Optional[Dict] = None,
    ) -> str:
        """Store an onboarding note for a user."""
        note_doc = {
            "user_id": user_id,
            "note_type": note_type,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = self.notes_collection.insert_one(note_doc)
        return str(result.inserted_id)

    def get_user_notes(
        self, user_id: str, note_type: Optional[str] = None
    ) -> List[Dict]:
        """Retrieve notes for a user, optionally filtered by type."""
        query = {"user_id": user_id}
        if note_type:
            query["note_type"] = note_type

        notes = list(self.notes_collection.find(query).sort("created_at", -1))

        # Convert ObjectId to string for JSON serialization
        for note in notes:
            note["_id"] = str(note["_id"])

        return notes

    def store_support_metadata(
        self,
        user_id: str,
        metadata_type: str,
        data: Dict,
        tags: Optional[List[str]] = None,
    ) -> str:
        """Store support metadata for a user."""
        metadata_doc = {
            "user_id": user_id,
            "metadata_type": metadata_type,
            "data": data,
            "tags": tags or [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = self.metadata_collection.insert_one(metadata_doc)
        return str(result.inserted_id)

    def update_onboarding_progress(
        self, user_id: str, step: str, status: str, details: Optional[Dict] = None
    ) -> str:
        """Update onboarding progress for a user."""
        progress_data = {
            "step": step,
            "status": status,
            "details": details or {},
            "timestamp": datetime.utcnow(),
        }

        # Store as metadata
        return self.store_support_metadata(
            user_id=user_id,
            metadata_type="onboarding_progress",
            data=progress_data,
            tags=["onboarding", "progress", step],
        )

    def get_onboarding_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive onboarding summary for a user."""
        # Get all notes
        notes = self.get_user_notes(user_id)

        # Get all metadata
        metadata = list(
            self.metadata_collection.find({"user_id": user_id}).sort("created_at", -1)
        )

        # Convert ObjectIds
        for item in metadata:
            item["_id"] = str(item["_id"])

        # Count by type
        note_types = {}
        for note in notes:
            note_type = note["note_type"]
            note_types[note_type] = note_types.get(note_type, 0) + 1

        metadata_types = {}
        for item in metadata:
            metadata_type = item["metadata_type"]
            metadata_types[metadata_type] = metadata_types.get(metadata_type, 0) + 1

        return {
            "user_id": user_id,
            "total_notes": len(notes),
            "total_metadata": len(metadata),
            "note_types": note_types,
            "metadata_types": metadata_types,
            "recent_notes": notes[:5],
            "recent_metadata": metadata[:5],
        }

    def search_notes(self, query: str, user_id: Optional[str] = None) -> List[Dict]:
        """Search notes by content."""
        search_query = {"$text": {"$search": query}}
        if user_id:
            search_query["user_id"] = user_id

        # Ensure text index exists
        try:
            self.notes_collection.create_index([("content", "text")])
        except:
            pass  # Index might already exist

        notes = list(self.notes_collection.find(search_query).sort("created_at", -1))

        for note in notes:
            note["_id"] = str(note["_id"])

        return notes

    def close(self):
        """Close MongoDB connection."""
        self.client.close()


# Helper function to get note store instance
def get_note_store() -> ProfileNoteStore:
    """Get configured ProfileNoteStore instance."""
    return ProfileNoteStore()
