import os
from database_client import get_firestore_client

def fetch_document(collection_name: str, document_id: str) -> dict | None:
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
        return doc.to_dict()
    else:
        print("No such document!")
        return None

if __name__ == "__main__":
    project_id = os.environ.get("FIRESTORE_PROJECT_ID")
    if not project_id:
        print("Please set the FIRESTORE_PROJECT_ID environment variable.")
    else:
        fetched_doc = fetch_document("my_collection", "doc_1")
        if fetched_doc:
            print(f"Successfully fetched document: {fetched_doc}")
