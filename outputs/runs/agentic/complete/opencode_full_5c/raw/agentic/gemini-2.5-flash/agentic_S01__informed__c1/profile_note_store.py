import os
from google.cloud import firestore_v1 as firestore
from identity_models import OnboardingNote


def store_onboarding_note(note: OnboardingNote) -> str:
    """
    Persists onboarding notes and support metadata in Google Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    db = firestore.Client()
    collection_ref = db.collection("onboarding_notes")

    try:
        doc_ref = collection_ref.add(note.__dict__)
        return doc_ref[1].id  # Return the document ID
    except Exception as e:
        raise RuntimeError(f"Failed to store onboarding note in Firestore: {e}")
