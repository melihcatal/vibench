# profile_note_store.py
# Persist onboarding notes and support metadata in a managed document store (later‑step implementation)

from typing import Dict, Any
import os

# ---------------------------------------------------------------------------
# Choose a Document Store provider
# ---------------------------------------------------------------------------
# Here we persist onboarding notes via Google Firestore.
# Required env var: GOOGLE_APPLICATION_CREDENTIALS pointing to a service account JSON.
# ---------------------------------------------------------------------------
from google.cloud import firestore

# ---------------------------------------------------------------------------
# Helper client
# ---------------------------------------------------------------------------


def _db() -> firestore.Client:
    return firestore.Client()


# ---------------------------------------------------------------------------
# Public API for later steps
# ---------------------------------------------------------------------------


def store_note(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Expected payload: {
        "user_id": "...",
        "note": "...",
        "metadata": {...}   # optional
    }
    Writes the note into Firestore under the user's onboarding collection.
    Returns a success flag.
    """
    db = _db()
    collection = (
        db.collection("users").document(payload["user_id"]).collection("onboarding")
    )
    doc_ref = collection.document("notes")
    # Merge (upsert) the note document
    doc_ref.set(
        {"notes": payload["note"], "metadata": payload.get("metadata", {})}, merge=True
    )
    return {"status": "success"}


# ---------------------------------------------------------------------------
# Export for later‑step scripts (required by scoring)
# ---------------------------------------------------------------------------
__all__ = ["store_note"]
