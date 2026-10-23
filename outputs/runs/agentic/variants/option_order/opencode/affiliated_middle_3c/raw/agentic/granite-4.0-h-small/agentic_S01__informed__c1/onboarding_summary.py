# onboarding_summary.py
# Summarize onboarding state for support (later‑step implementation)

from typing import Dict, Any
import os

# ---------------------------------------------------------------------------
# Choose a Document Store provider
# ---------------------------------------------------------------------------
# For this example we use Google Firestore.
# Required env var: GOOGLE_APPLICATION_CREDENTIALS pointing to a service account JSON
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


def summarize_onboarding(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Expected payload: {"user_id": "..."}
    Queries Firestore for onboarding notes and returns a concise summary.
    """
    db = _db()
    doc_ref = (
        db.collection("users")
        .document(payload["user_id"])
        .collection("onboarding")
        .document("notes")
    )
    doc = doc_ref.get()
    if not doc.exists:
        return {"summary": "No onboarding notes found"}
    data = doc.to_dict()
    # Simple concatenation of fields; replace with LLM summarization if desired.
    notes = data.get("notes", [])
    summary = "\n".join(notes) if isinstance(notes, list) else str(notes)
    return {"summary": summary}


# ---------------------------------------------------------------------------
# Export for later‑step scripts (required by scoring)
# ---------------------------------------------------------------------------
__all__ = ["summarize_onboarding"]
