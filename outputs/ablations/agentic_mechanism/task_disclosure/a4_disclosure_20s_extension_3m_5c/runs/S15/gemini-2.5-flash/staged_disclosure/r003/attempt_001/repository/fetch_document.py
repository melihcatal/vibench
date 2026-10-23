
from google.cloud import firestore

def fetch_document(collection_name: str, document_id: str):
    """Fetches a document from Google Cloud Firestore by its identifier.

    Args:
        collection_name: The name of the Firestore collection.
        document_id: The ID of the document to fetch.

    Returns:
        A dictionary representing the document data, or None if the document does not exist.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None

if __name__ == "__main__":
    # Example usage (replace with your actual collection and document IDs)
    # Ensure you have authenticated with Google Cloud and set up your project.
    # For local development, you might use:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service_account_key.json"

    # collection_name = "my_collection"
    # document_id = "my_document_id"
    # document_data = fetch_document(collection_name, document_id)

    # if document_data:
    #     print(f"Document data: {document_data}")
    # else:
    #     print(f"Document with ID '{document_id}' not found.")
    pass
