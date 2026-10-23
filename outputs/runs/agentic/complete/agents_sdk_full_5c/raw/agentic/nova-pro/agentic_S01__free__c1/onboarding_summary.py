import firebase_admin
from firebase_admin import firestore

def onboarding_summary(user_id):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    db = firestore.client()
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    return user_doc.to_dict()