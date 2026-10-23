from google.cloud import firestore


def record_text_safety(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    doc = client.collection(config["collection"]).document(payload["id"]).get()
    data = doc.to_dict() if doc.exists else {}
    text = " ".join(str(v).lower() for v in data.values() if isinstance(v, str))
    unsafe = any(term in text for term in ["password", "ssn", "credit card", "secret"])
    return {"id": payload["id"], "safe": not unsafe}
