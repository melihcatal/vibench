from google.cloud import firestore


def profile_note_store(payload, config=None):
    client = firestore.Client(project=(config or {}).get("project_id"))
    doc = client.collection("onboarding_notes").document(payload["user_id"])
    doc.set({"notes": payload.get("notes", ""), "metadata": payload.get("metadata", {}), "status": payload.get("status", "")}, merge=True)
    return {"stored": True, "user_id": payload["user_id"]}
