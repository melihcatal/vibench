from google.cloud import firestore

db = firestore.Client()

def store_profile_note(user_id, note):
    doc_ref = db.collection('profile_notes').document(user_id)
    doc_ref.set({'note': note})