import os
from google.cloud import firestore
from typing import Dict, Any, List, Optional
from datetime import datetime


def store_onboarding_note(
    user_id: str,
    note_type: str,
    content: Dict[str, Any],
    metadata: Dict[str, Any] = None,
) -> str:
    """Persist onboarding notes and support metadata in Firestore."""
    try:
        # Initialize Firestore client
        # Google Cloud credentials are automatically loaded from environment
        db = firestore.Client()

        # Create note document
        note_data = {
            "user_id": user_id,
            "note_type": note_type,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "provider": "firestore",
        }

        # Add to Firestore collection
        doc_ref = db.collection("onboarding_notes").document()
        doc_ref.set(note_data)

        return doc_ref.id
    except Exception as e:
        raise RuntimeError(f"Failed to store onboarding note: {str(e)}")


def get_user_notes(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve onboarding notes for a specific user."""
    try:
        db = firestore.Client()

        # Query notes for user
        notes_query = (
            db.collection("onboarding_notes")
            .where("user_id", "==", user_id)
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .limit(limit)
        )

        notes = []
        for doc in notes_query.stream():
            note_data = doc.to_dict()
            note_data["id"] = doc.id
            notes.append(note_data)

        return notes
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve user notes: {str(e)}")


def update_note_metadata(note_id: str, metadata_updates: Dict[str, Any]) -> bool:
    """Update metadata for an existing note."""
    try:
        db = firestore.Client()

        doc_ref = db.collection("onboarding_notes").document(note_id)

        # Update metadata and timestamp
        updates = {
            "metadata": metadata_updates,
            "updated_at": datetime.utcnow().isoformat(),
        }

        doc_ref.update(updates)
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to update note metadata: {str(e)}")


def store_support_interaction(
    user_id: str, interaction_type: str, details: Dict[str, Any]
) -> str:
    """Store support interaction in Firestore."""
    try:
        db = firestore.Client()

        interaction_data = {
            "user_id": user_id,
            "interaction_type": interaction_type,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
            "provider": "firestore",
        }

        doc_ref = db.collection("support_interactions").document()
        doc_ref.set(interaction_data)

        return doc_ref.id
    except Exception as e:
        raise RuntimeError(f"Failed to store support interaction: {str(e)}")


def get_user_support_history(user_id: str, days: int = 30) -> List[Dict[str, Any]]:
    """Get support interaction history for a user."""
    try:
        db = firestore.Client()

        # Calculate cutoff date
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Query support interactions
        interactions_query = (
            db.collection("support_interactions")
            .where("user_id", "==", user_id)
            .where("timestamp", ">=", cutoff_date.isoformat())
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
        )

        interactions = []
        for doc in interactions_query.stream():
            interaction_data = doc.to_dict()
            interaction_data["id"] = doc.id
            interactions.append(interaction_data)

        return interactions
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve support history: {str(e)}")


def create_onboarding_checkpoint(user_id: str, checkpoint_data: Dict[str, Any]) -> str:
    """Create an onboarding checkpoint record."""
    try:
        db = firestore.Client()

        checkpoint = {
            "user_id": user_id,
            "checkpoint_data": checkpoint_data,
            "created_at": datetime.utcnow().isoformat(),
            "status": "active",
            "provider": "firestore",
        }

        doc_ref = db.collection("onboarding_checkpoints").document()
        doc_ref.set(checkpoint)

        return doc_ref.id
    except Exception as e:
        raise RuntimeError(f"Failed to create onboarding checkpoint: {str(e)}")
