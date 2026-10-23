from google.cloud import firestore
from database_client import get_firestore_client

def query_documents(collection_name: str, field: str, value: any, config: dict = None):
    config = config or {}
    client = get_firestore_client(project_id=config["project_id"])
    docs_ref = client.collection(collection_name).where(field, "==", value).stream()
    results = []
    for doc in docs_ref:
        results.append({"id": doc.id, "document": doc.to_dict()})
    return results
