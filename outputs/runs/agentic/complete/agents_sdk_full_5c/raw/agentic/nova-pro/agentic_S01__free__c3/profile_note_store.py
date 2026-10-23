import os
import firebase_admin
from firebase_admin import firestore

cred = firebase_admin.credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def store_note(user_id, note):
    db.collection('users').document(user_id).set({'note': note}, merge=True)