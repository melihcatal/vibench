from google.cloud import firestore
import os
from database_models import Document


def query_documents(collection_name: str, field: str, value: any):
    db = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    docs_ref = db.collection(collection_name).where(field, "==", value).stream()
    results = []
    for doc in docs_ref:
        results.append(
            Document(collection_name=collection_name, id=doc.id, data=doc.to_dict())
        )
    return results
