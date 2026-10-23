import os
from google.cloud import firestore

def store_profile_note(user_id, note):
    client = firestore.Client()
    doc_ref = client.collection(u'profile_notes').document(user_id)
    doc_ref.set({'note': note})