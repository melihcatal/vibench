from google.cloud import firestore
from identity_models import UserProfile
import os

# Initialize Firestore client with provider-specific project ID
db = firestore.Client(project=os.getenv("FIREBASE_PROJECT_ID"))


def profile_note_store(profile: UserProfile, notes: str) -> bool:
    try:
        doc_ref = db.collection("user_notes").document(profile.user_id)
        doc_ref.set(
            {
                "user_id": profile.user_id,
                "email": profile.email,
                "notes": notes,
                "updated_at": firestore.SERVER_TIMESTAMP,
            }
        )
        return True
    except Exception:
        return False
