import os
import firebase_admin
from firebase_admin import firestore

cred = firebase_admin.credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def summarize_onboarding(user_id):
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get().to_dict()
    return user_doc