from google.cloud import firestore
import os

def persist_message_record(record: dict):
    """
    Persists a processed message record to Google Cloud Firestore.
    """
    # Initialize Firestore client
    db = firestore.Client()

    # Reference to a collection
    # You might want to make the collection name configurable or dynamically generated
    collection_ref = db.collection(os.environ.get("FIRESTORE_COLLECTION_NAME", "message_audit_records"))

    # Add a new document with a generated ID
    doc_ref = collection_ref.add(record)
    print(f"Record added with ID: {doc_ref[1].id}")

