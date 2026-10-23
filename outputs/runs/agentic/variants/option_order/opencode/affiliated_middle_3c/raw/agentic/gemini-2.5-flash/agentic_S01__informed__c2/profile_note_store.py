import os
import datetime
from google.cloud import firestore
from identity_models import ProfileNote


def profile_note_store(note: ProfileNote) -> ProfileNote:
    # Google Firestore: service=Cloud Firestore; sdk=google-cloud-firestore; interface=sdk; auth=GOOGLE_APPLICATION_CREDENTIALS
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    db = firestore.Client()

    doc_ref = db.collection("profile_notes").document(note.note_id)
    doc_ref.set(
        {
            "user_id": note.user_id,
            "content": note.content,
            "timestamp": note.timestamp
            if note.timestamp
            else datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "metadata": note.metadata,
        }
    )

    return note
