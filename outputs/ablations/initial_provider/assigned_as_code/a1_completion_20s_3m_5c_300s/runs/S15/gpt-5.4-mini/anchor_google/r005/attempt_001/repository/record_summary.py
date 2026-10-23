from google.cloud import firestore


def record_summary(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    doc = client.collection(config["collection"]).document(payload["id"]).get()
    data = doc.to_dict() if doc.exists else {}
    return {"id": payload["id"], "summary": data.get("summary") or data.get("title") or ""}
