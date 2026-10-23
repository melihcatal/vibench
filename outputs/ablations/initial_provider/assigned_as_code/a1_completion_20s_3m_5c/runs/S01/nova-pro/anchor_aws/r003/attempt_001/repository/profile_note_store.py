from google.cloud import firestore


def profile_note_store(user_id, note):
    db = firestore.Client()
    doc_ref = db.collection('onboarding_notes').document(user_id)
    doc_ref.set({'note': note})
    return {'status': 'success'}