from google.cloud import firestore

from database_client import load_config
from database_models import normalize_document


def record_text_safety(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    snapshot = client.collection(config["collection"]).document(payload["id"]).get()
    document = normalize_document(snapshot) or {}
    text = " ".join(str(document.get(field, "")) for field in payload.get("fields", ["text"]))
    unsafe = any(token in text.lower() for token in ["<script", "drop table", "--", "javascript:"])
    return {"id": payload["id"], "unsafe": unsafe}
