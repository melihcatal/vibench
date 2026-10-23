from google.cloud import firestore

from database_client import load_config
from database_models import build_document_response


def fetch_document(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    snapshot = client.collection(config["collection"]).document(payload["id"]).get()
    return build_document_response(payload["id"], snapshot.to_dict() or {})
