from google.cloud import firestore

def upsert_document(collection_name: str, document_id: str, document_data: dict):
    """Upserts a JSON document into a Firestore collection by its primary identifier.

    Args:
        collection_name: The name of the Firestore collection.
        document_id: The ID of the document to upsert.
        document_data: The dictionary representing the JSON document to upsert.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(document_data)
    print(f"Document {document_id} upserted in collection {collection_name}.")

