from google.cloud import firestore


def profile_note_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config.get("project_id"))
    doc = client.collection(config.get("collection", "onboarding_notes")).document(payload["user_id"])
    doc.set({"notes": payload.get("notes"), "metadata": payload.get("metadata", {}), "user_id": payload["user_id"]}, merge=True)
    return {"stored": True, "document_id": payload["user_id"]}
