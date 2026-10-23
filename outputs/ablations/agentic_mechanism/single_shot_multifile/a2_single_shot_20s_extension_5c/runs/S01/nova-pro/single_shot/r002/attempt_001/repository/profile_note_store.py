import os
from google.cloud import firestore

def store_profile_note(user_id, note):
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    db = firestore.Client(project=project_id)
    doc_ref = db.collection('profile_notes').document(user_id)
    doc_ref.set({'note': note})
    return doc_ref.id