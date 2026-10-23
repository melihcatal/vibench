import os
import json
from google.cloud import firestore
from identity_models import NormalizedUser


def store_onboarding_notes(user: NormalizedUser, notes: dict) -> None:
    """Persists onboarding notes and support metadata in Firestore.

    Creates/updates a document under the collection 'onboarding_profiles' using
    the user's email address as the document ID. Stores the full notes dict
    alongside a snapshot of the user record.
    """
    db = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var for auth
    doc_ref = db.collection("onboarding_profiles").document(user["Email"])
    doc_ref.set(
        {"user": user, "notes": notes, "updated_at": firestore.SERVER_TIMESTAMP}
    )
    print(f"Stored onboarding notes for {user['Email']} in Firestore.")
