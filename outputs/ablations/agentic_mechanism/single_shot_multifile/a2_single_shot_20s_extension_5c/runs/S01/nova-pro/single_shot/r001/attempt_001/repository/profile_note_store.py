import os
from google.cloud import firestore

def store_note(user_id, note):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    db = firestore.Client()
    user_ref = db.collection('users').document(user_id)
    user_ref.set({'note': note}, merge=True)