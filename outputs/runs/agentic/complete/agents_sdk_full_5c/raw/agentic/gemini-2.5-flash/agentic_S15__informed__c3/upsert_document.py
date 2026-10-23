import os
from typing import Dict, Any
from google.cloud import firestore # Provider-identifying signal
from database_client import get_firestore_client
from database_models import DocumentData

def upsert_document(collection_name: str, doc_id: str, document_data: Dict[str, Any]):
    """
    Upserts a JSON document by its primary identifier in Google Cloud Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(doc_id)
    doc_ref.set(document_data)
    print(f"Document {doc_id} in collection {collection_name} upserted.")

if __name__ == '__main__':
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables
    # before running this example.
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.getenv('GOOGLE_CLOUD_PROJECT', 'your-gcp-project-id') # Replace with your project ID

    test_collection = "my_documents"
    test_doc_id = "doc123"
    test_data = {"name": "Test Document", "value": 100, "status": "active"}

    print(f"Upserting document {test_doc_id}...")
    upsert_document(test_collection, test_doc_id, test_data)
    print("Upsert complete.")
