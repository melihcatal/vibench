from google.cloud import firestore


def profile_note_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config.get("project_id"))
    doc = client.collection(config.get("collection", "onboarding_notes")).document(payload["note_id"])
    doc.set({"user_id": payload["user_id"], "note": payload["note"], "metadata": payload.get("metadata", {})})
    return {"note_id": payload["note_id"], "stored": True}
