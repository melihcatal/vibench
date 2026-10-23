from database_client import get_firestore_client, load_config
from database_models import build_response


def query_documents(payload, config=None):
    config = load_config(config)
    client = get_firestore_client(config)
    field = payload["field"]
    value = payload["value"]
    query = client.collection(config["collection"]).where(field, "==", value)
    documents = [snapshot.to_dict() for snapshot in query.stream()]
    return build_response(documents=documents)
