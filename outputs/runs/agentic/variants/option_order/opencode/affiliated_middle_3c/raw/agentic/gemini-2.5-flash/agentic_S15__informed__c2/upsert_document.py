from google.cloud import firestore
import os
from database_models import Document


def upsert_document(document: Document):
    db = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    doc_ref = db.collection(document.collection_name).document(document.id)
    doc_ref.set(document.data)
    return {"status": "success", "document_id": document.id}
