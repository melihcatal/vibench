from database_client import get_firestore_client

def query_documents(payload, config=None):
    config = config or {}
    client = get_firestore_client(project_id=config["project_id"])
    query = client.collection(config["collection"]).where(payload["field"], "==", payload["value"])
    results = []
    for doc in query.stream():
        results.append({"id": doc.id, "document": doc.to_dict()})
    return {"documents": results}
