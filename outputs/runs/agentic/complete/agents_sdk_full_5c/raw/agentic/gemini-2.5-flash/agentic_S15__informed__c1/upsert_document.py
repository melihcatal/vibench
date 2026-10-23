import os
from database_client import get_firestore_client

def upsert_document(collection_name: str, document_id: str, data: dict):
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    print(f"Document {document_id} in collection {collection_name} upserted.")

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for local testing
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    # export FIRESTORE_PROJECT_ID="your-gcp-project-id"
    project_id = os.environ.get("FIRESTORE_PROJECT_ID")
    if not project_id:
        print("Please set the FIRESTORE_PROJECT_ID environment variable.")
    else:
        sample_data = {"name": "Test Document", "value": 123, "status": "active"}
        upsert_document("my_collection", "doc_1", sample_data)
