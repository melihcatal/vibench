from google.cloud import firestore


def record_summary(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    doc = client.collection(config["collection"]).document(payload["id"]).get()
    data = doc.to_dict() if doc.exists else {}
    text = " ".join(str(v) for v in data.values() if isinstance(v, (str, int, float, bool)))
    return {"id": payload["id"], "summary": text[:280]}
