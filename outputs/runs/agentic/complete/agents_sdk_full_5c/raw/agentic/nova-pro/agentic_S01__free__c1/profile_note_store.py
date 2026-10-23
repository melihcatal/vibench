import firebase_admin
from firebase_admin import firestore

def profile_note_store(user_id, note):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    db = firestore.client()
    user_ref = db.collection('users').document(user_id)
    user_ref.set({'note': note}, merge=True)