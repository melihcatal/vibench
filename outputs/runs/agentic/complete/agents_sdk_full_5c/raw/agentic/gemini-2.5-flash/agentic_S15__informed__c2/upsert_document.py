from database_client import get_firestore_client
from database_models import Document

def upsert_document(collection_name: str, document: Document):
    """Upserts a JSON document by its primary identifier into Firestore.

    Args:
        collection_name: The name of the Firestore collection.
        document: The Document object to upsert.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document.id)
    doc_ref.set(document.to_dict())
    print(f"Document with ID {document.id} upserted in collection {collection_name}.")
