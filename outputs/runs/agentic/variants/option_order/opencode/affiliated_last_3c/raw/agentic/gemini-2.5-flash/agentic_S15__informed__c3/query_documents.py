from database_client import get_firestore_client


def query_documents(collection_name: str, field_name: str, field_value: str):
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    results = []
    for doc in docs:
        results.append({"id": doc.id, **doc.to_dict()})
    return results
