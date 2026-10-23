import os
from database_client import get_firestore_client

def query_documents(collection_name: str, field: str, value: any) -> list[dict]:
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field, "==", value).stream()
    results = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        results.append(doc_data)
    print(f"Found {len(results)} documents matching query: {results}")
    return results

if __name__ == "__main__":
    project_id = os.environ.get("FIRESTORE_PROJECT_ID")
    if not project_id:
        print("Please set the FIRESTORE_PROJECT_ID environment variable.")
    else:
        # Example: Query for documents where 'status' is 'active'
        active_docs = query_documents("my_collection", "status", "active")
        if active_docs:
            print(f"Active documents: {active_docs}")
