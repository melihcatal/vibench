from google.cloud import firestore
import os
from database_models import Document


def fetch_document(collection_name: str, document_id: str):
    db = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return Document(
            collection_name=collection_name, id=document_id, data=doc.to_dict()
        )
    else:
        return None
