import os
from typing import Optional, Dict, Any
from google.cloud import firestore # Provider-identifying signal
from database_client import get_firestore_client
from database_models import DocumentData

def fetch_document(collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a document by identifier from Google Cloud Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(doc_id)
    document = doc_ref.get()

    if document.exists:
        print(f"Document {doc_id} in collection {collection_name} fetched.")
        return document.to_dict()
    else:
        print(f"Document {doc_id} not found in collection {collection_name}.")
        return None

if __name__ == '__main__':
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables
    # before running this example.
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.getenv('GOOGLE_CLOUD_PROJECT', 'your-gcp-project-id') # Replace with your project ID

    test_collection = "my_documents"
    test_doc_id = "doc123"

    print(f"Fetching document {test_doc_id}...")
    fetched_data = fetch_document(test_collection, test_doc_id)

    if fetched_data:
        print("Fetched data:", fetched_data)
    else:
        print("No document found.")
