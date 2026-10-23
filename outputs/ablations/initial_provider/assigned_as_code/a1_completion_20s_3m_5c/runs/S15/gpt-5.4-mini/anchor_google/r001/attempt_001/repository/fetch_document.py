from database_client import get_firestore_client, load_config
from database_models import build_response


def fetch_document(payload, config=None):
    config = load_config(config)
    client = get_firestore_client(config)
    snapshot = client.collection(config["collection"]).document(payload["id"]).get()
    document = snapshot.to_dict() if snapshot.exists else None
    return build_response(id=payload["id"], document=document)
