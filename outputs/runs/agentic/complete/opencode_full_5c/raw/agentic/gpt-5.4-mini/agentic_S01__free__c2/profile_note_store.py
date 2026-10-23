import os
from google.cloud import firestore

FIRESTORE_COLLECTION = 'onboarding_notes'


def profile_note_store(note_id, payload):
    db = firestore.Client(project=os.environ.get('GOOGLE_CLOUD_PROJECT'))
    doc = db.collection(FIRESTORE_COLLECTION).document(note_id)
    doc.set(payload)
    return {'note_id': note_id, 'stored': True}
