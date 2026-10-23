from google.cloud import firestore


def upsert_document(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    client.collection(config["collection"]).document(payload["id"]).set(payload["document"])
    return {"id": payload["id"]}
