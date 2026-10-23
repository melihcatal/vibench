from google.cloud import firestore


def query_documents(field, value, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    query = client.collection(config["collection"]).where(field, "==", value).stream()
    results = [doc.to_dict() for doc in query]
    return results