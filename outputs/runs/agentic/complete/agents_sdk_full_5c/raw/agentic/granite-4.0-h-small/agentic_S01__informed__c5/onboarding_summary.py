import os
import json
from identity_client import IdentityClient
from identity_models import IdentityError

# Use Google Cloud Firestore as the document store for onboarding metadata
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

from google.cloud import firestore

DB = firestore.Client()

def onboarding_summary(user_id: str) -> str:
    """Create a support-friendly summary of the user's onboarding state.

    Collects profile fields, moderation status, and any persisted notes from Firestore.
    Returns a simple markdown string.
    Raises IdentityError if Firestore communication fails.
    """
    doc_ref = DB.collection('users').document(user_id)
    user_doc = doc_ref.get()
    if not user_doc.exists:
        raise IdentityError(f"User document not found: {user_id}")
    data = user_doc.to_dict()
    summary_lines = [
        f"## Onboarding Summary for {user_doc.id}"
    ]
    summary_lines.append(f"- **Email:** {data.get('email', 'N/A')}" )
    summary_lines.append(f"- **Locale:** {data.get('locale', 'N/A')}" )
    summary_lines.append(f"- **Profile Moderation:** {data.get('moderation_status', 'Pending')}" )
    notes_ref = doc_ref.collection('notes').document('onboarding').get()
    notes = notes_ref.to_dict() or {}
    notes_text = notes.get('text', '')
    summary_lines.append(f"- **Onboarding Notes:**\n{notes_text}")
    return '\\n'.join(summary_lines)
