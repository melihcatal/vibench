from google.cloud import firestore

db = firestore.Client()

def profile_note_store(user_id, note):
    doc_ref = db.collection(u'profile_notes').document(user_id)
    doc_ref.set({'note': note})
    return 'Note stored successfully'