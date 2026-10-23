from google.cloud import firestore

from database_client import load_config


def record_translate(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    snapshot = client.collection(config["collection"]).document(payload["id"]).get()
    document = snapshot.to_dict() or {}
    translated = dict(document)
    if "title" in translated:
        translated["title"] = translated["title"]
    if "description" in translated:
        translated["description"] = translated["description"]
    return {"id": payload["id"], "document": translated}
