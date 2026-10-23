from google.cloud import firestore
from identity_models import OnboardingNote
import uuid
import datetime

def save_onboarding_note(user_id: str, note_content: str) -> OnboardingNote:
    """
    Saves a note related to user onboarding in Google Cloud Firestore.
    
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    db = firestore.Client()
    
    note_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()

    doc_ref = db.collection(u'onboarding_notes').document(note_id)
    
    note_data = {
        u'user_id': user_id,
        u'note_id': note_id,
        u'content': note_content,
        u'timestamp': timestamp
    }
    
    doc_ref.set(note_data)
    
    return OnboardingNote(
        user_id=user_id,
        note_id=note_id,
        content=note_content,
        timestamp=timestamp
    )
