from typing import Dict, Any
from google.cloud import firestore
from database_client import get_firestore_client

def upsert_document(collection_name: str, document_id: str, document_data: Dict[str, Any]):
    """Upserts a JSON document into a specified Firestore collection.

    Args:
        collection_name (str): The name of the Firestore collection.
        document_id (str): The ID of the document to upsert.
        document_data (Dict[str, Any]): The JSON data for the document.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    try:
        doc_ref.set(document_data)
        print(f"Document {document_id} upserted successfully in collection {collection_name}.")
    except Exception as e:
        print(f"Error upserting document {document_id}: {e}")
        raise

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or running in a GC environment
    # For local testing, ensure Firestore emulator is running or credentials are set up.
    sample_doc_id = "product123"
    sample_doc_data = {
        "name": "Wireless Bluetooth Headphones",
        "brand": "AudioTech",
        "price": 99.99,
        "features": ["Noise Cancellation", "30-hour battery", "Water Resistant"],
        "available": True
    }
    collection = "products"

    print(f"Attempting to upsert document {sample_doc_id}...")
    try:
        upsert_document(collection, sample_doc_id, sample_doc_data)

        # Update an existing document
        updated_doc_data = {
            "name": "Wireless Bluetooth Headphones Pro",
            "price": 129.99,
            "available": False,
            "color": "Black"
        }
        upsert_document(collection, sample_doc_id, updated_doc_data)

    except Exception as e:
        print(f"Example usage failed: {e}")
