from google.cloud import firestore

from database_client import load_config


def record_text_safety(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    snapshot = client.collection(config["collection"]).document(payload["id"]).get()
    document = snapshot.to_dict() or {}
    text = " ".join(str(value) for value in document.values() if isinstance(value, str)).lower()
    unsafe = any(term in text for term in ["self-harm", "hate", "violence", "sexual"])
    return {"id": payload["id"], "safe": not unsafe}
