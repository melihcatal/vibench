import os
from google.cloud import firestore


def profile_note_store(user_id, note):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "path/to/your/service-account-file.json"
    )
    db = firestore.Client()
    user_ref = db.collection("users").document(user_id)
    user_ref.set({"note": note})
