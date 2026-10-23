from google.cloud import firestore
import datetime


def profile_note_store(user_id: str, note_content: str, metadata: dict) -> None:
    db = firestore.Client()

    doc_ref = db.collection("profilenotes").document(user_id)

    note_data = {
        "content": note_content,
        "metadata": metadata,
        "created_at": datetime.datetime.now(datetime.timezone.utc),
    }

    doc_ref.set(note_data, merge=True)
