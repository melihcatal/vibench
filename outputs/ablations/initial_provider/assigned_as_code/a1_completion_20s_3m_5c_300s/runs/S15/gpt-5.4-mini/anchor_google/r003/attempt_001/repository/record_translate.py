from google.cloud import firestore


def record_translate(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    doc = client.collection(config["collection"]).document(payload["id"]).get()
    data = doc.to_dict() if doc.exists else {}
    target_language = payload.get("target_language", "en")
    translated = dict(data)
    translated["language"] = target_language
    return {"id": payload["id"], "document": translated}
