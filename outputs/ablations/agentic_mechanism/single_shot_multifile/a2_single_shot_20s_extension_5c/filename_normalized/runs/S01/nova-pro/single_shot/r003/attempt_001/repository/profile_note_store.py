import os
from firebase_admin import firestore, credentials

cred = credentials.Certificate("path/to/serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def store_profile_note(user_id, note):
    doc_ref = db.collection('profile_notes').document(user_id)
    doc_ref.set({'note': note})
    return doc_ref.id