from google.cloud import firestore

from database_client import load_config
from database_models import normalize_document


def record_summary(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    snapshot = client.collection(config["collection"]).document(payload["id"]).get()
    document = normalize_document(snapshot) or {}
    return {"id": payload["id"], "summary": document.get("summary") or document.get("title") or ""}
