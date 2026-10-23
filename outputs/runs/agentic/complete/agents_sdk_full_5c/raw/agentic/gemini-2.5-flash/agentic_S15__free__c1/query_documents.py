from google.cloud import firestore
import os

def query_documents(collection_name: str, field_name: str, field_value: str):
    """Queries documents by a field value or partition-style key in Firestore."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    db = firestore.Client(project=project_id)
    docs = (
        db.collection(collection_name)
        .where(field_name, "==", field_value)
        .stream()
    )
    results = []
    for doc in docs:
        results.append({"id": doc.id, **doc.to_dict()})
    return {"status": "success", "documents": results}
