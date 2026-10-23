import firebase_admin
from firebase_admin import firestore

from identity_models import build_account_payload


def profile_note_store(payload, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    data = build_account_payload(payload)
    db = firestore.client(app=app)
    doc = db.collection("onboarding_notes").document(data["email"] or payload["user_id"])
    doc.set({"user_id": payload.get("user_id"), "note": data["note"], "metadata": payload.get("metadata", {})}, merge=True)
    return {"stored": True, "document_id": doc.id}
