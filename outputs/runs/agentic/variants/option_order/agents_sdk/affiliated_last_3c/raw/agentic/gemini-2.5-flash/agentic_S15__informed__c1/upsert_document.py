from google.cloud import firestore
from database_client import get_firestore_client
from database_models import Document

def upsert_document(document: Document):
    """Upserts a JSON document into Firestore by its primary identifier."""
    db = get_firestore_client()
    doc_ref = db.collection(document.collection_name).document(document.doc_id)
    doc_ref.set(document.data)
    print(f"Document {document.doc_id} upserted in collection {document.collection_name}.")

if __name__ == '__main__':
    # Example usage (requires Firestore emulator or live project setup)
    # from google.cloud import firestore_v1
    # # For local emulator:
    # # import os
    # # os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    #
    # doc_to_upsert = Document(
    #     collection_name="my_collection",
    #     doc_id="doc123",
    #     data={"title": "My First Document", "content": "This is some content."}
    # )
    # upsert_document(doc_to_upsert)
    pass
