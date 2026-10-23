import os

from database_client import get_firestore_client
from database_models import QueryRequest


def query_documents(request: QueryRequest):
    client = get_firestore_client()
    docs = client.collection(request.collection).where(request.field_name, "==", request.field_value).stream()
    results = []
    for doc in docs:
        data = doc.to_dict() or {}
        data["id"] = doc.id
        results.append(data)
    return {"ok": True, "documents": results}


def main():
    request = QueryRequest(collection=os.getenv("FIRESTORE_COLLECTION", "documents"), field_name="status", field_value="active")
    return query_documents(request)


if __name__ == "__main__":
    main()
