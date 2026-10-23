import os
from google.cloud import firestore

def store_profile_note(user_id, note):
    if not firestore._apps:
        firestore.Client.create(project=os.getenv('FIRESTORE_PROJECT'))
    db = firestore.client()
    doc_ref = db.collection('profile_notes').document(user_id)
    doc_ref.set({'note': note})