from google.cloud import firestore

from database_client import load_config


def record_summary(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    snapshot = client.collection(config["collection"]).document(payload["id"]).get()
    document = snapshot.to_dict() or {}
    text = document.get("title") or document.get("name") or ""
    return {"id": payload["id"], "summary": text[:160], "fields": len(document)}
