from google.cloud import firestore

from database_client import load_config
from database_models import normalize_document


def query_documents(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    field = payload["field"]
    value = payload["value"]
    query = client.collection(config["collection"]).where(filter=firestore.FieldFilter(field, "==", value))
    return [normalize_document(doc) for doc in query.stream()]
