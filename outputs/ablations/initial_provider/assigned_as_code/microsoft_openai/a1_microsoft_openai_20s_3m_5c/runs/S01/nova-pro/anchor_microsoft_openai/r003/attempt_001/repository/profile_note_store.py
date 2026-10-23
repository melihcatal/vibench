import firebase_admin
from firebase_admin import credentials, firestore

def store_note(note):
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    db.collection('onboarding_notes').add(note)
