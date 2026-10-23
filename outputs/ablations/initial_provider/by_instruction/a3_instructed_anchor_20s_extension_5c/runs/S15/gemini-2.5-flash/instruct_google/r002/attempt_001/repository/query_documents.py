from database_client import get_firestore_client

def query_documents(collection_name: str, field_name: str, field_value: any):
    db = get_firestore_client()
    query = db.collection(collection_name).where(field_name, "==", field_value).stream()
    results = []
    for doc in query:
        results.append({"document_id": doc.id, "data": doc.to_dict()})
    return {"status": "success", "results": results}