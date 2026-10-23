import firebase_admin
from firebase_admin import firestore

def initialize_firestore():
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    db = firestore.client()
    return db

def store_onboarding_notes(user_id, notes):
    db = initialize_firestore()
    doc_ref = db.collection('onboarding_notes').document(user_id)
    doc_ref.set({'notes': notes})