from google.cloud import firestore


def store_profile_note(note):
    db = firestore.Client(project="your_project_id")
    doc_ref = db.collection("onboarding_notes").document()
    doc_ref.set(note)
