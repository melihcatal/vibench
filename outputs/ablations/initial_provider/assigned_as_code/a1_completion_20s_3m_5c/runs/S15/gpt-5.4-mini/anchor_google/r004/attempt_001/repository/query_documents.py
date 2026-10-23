from google.cloud import firestore

from database_client import load_config
from database_models import build_query_response


def query_documents(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    field = payload["field"]
    value = payload["value"]
    docs = []
    for snapshot in client.collection(config["collection"]).where(field, "==", value).stream():
        docs.append({"id": snapshot.id, "document": snapshot.to_dict() or {}})
    return build_query_response(docs)
