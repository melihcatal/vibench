import os
from google.cloud import firestore
from identity_client import IdentityClient
from identity_models import IdentityError

# Use Google Cloud Firestore as the managed document store for onboarding notes
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
DB = firestore.Client()

def store_onboarding_note(user_id: str, note_text: str, metadata: dict = None) -> None:
    """Persist onboarding notes and optional metadata in Firestore.

    Creates/updates a subcollection \"notes\" under the user document with a single document \"onboarding\".
    Metadata is stored alongside the note text.
    Raises IdentityError on write failure.
    """
    doc_ref = DB.collection('users').document(user_id)
    note_ref = doc_ref.collection('notes').document('onboarding')
    payload = {
        'text': note_text,
        'timestamp': firestore.SERVER_TIMESTAMP,
    }
    if metadata:
        payload['metadata'] = metadata
    note_ref.set(payload)
