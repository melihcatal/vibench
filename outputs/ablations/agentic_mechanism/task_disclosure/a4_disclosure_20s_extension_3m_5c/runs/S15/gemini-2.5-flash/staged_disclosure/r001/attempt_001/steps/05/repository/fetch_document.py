import os
from google.cloud import firestore

def fetch_document_from_firestore(collection_name: str, document_id: str) -> dict | None:
    """
    Fetches a document by its identifier from a Google Cloud Firestore collection.

    Args:
        collection_name: The name of the Firestore collection.
        document_id: The ID of the document to fetch.

    Returns:
        A dictionary representing the document data if found, otherwise None.
    """
    # Initialize Firestore client
    # The project ID is typically determined from the GOOGLE_CLOUD_PROJECT environment variable
    # or from the active gcloud configuration.
    db = firestore.Client()

    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None

if __name__ == "__main__":
    # Example usage (replace with your actual collection and document IDs)
    # Ensure GOOGLE_CLOUD_PROJECT environment variable is set or gcloud is configured
    # For local development, you might need to set GOOGLE_APPLICATION_CREDENTIALS
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    collection = "my_documents"  # Replace with your collection name
    doc_id = "document_123"  # Replace with your document ID

    document_data = fetch_document_from_firestore(collection, doc_id)

    if document_data:
        print(f"Document data: {document_data}")
    else:
        print(f"Document with ID '{doc_id}' not found in collection '{collection}'.")
