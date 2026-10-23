from google.cloud import firestore
import os
import datetime

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

def profile_note_store(note):
    db = firestore.Client(project=GOOGLE_CLOUD_PROJECT)
    doc_ref = db.collection(u'onboarding_notes').document()
    doc_ref.set({
        u'user_id': note.user_id,
        u'note_content': note.note_content,
        u'created_by': note.created_by,
        u'created_at': datetime.datetime.now()
    })
    return {"note_id": doc_ref.id}
