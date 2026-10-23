import os, json
from google.cloud import firestore

def store_note(user_id, note_text, metadata=None):
    # Google Firestore credentials via GOOGLE_APPLICATION_CREDENTIALS env var
    db = firestore.Client()
    doc_ref = db.collection('users').document(user_id)
    data = {'notes': note_text}
    if metadata:
        data.update(metadata)
    doc_ref.set(data, merge=True)
    return {'status': 'stored', 'document_id': doc_ref.id}
